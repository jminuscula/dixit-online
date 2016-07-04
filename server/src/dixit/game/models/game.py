
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from dixit import settings
from dixit.utils import ChoicesEnum
from dixit.game.exceptions import GameDeckExhausted, GameRoundIncomplete, GameFinished


class GameStatus(ChoicesEnum):
    NEW = 'new'
    ONGOING = 'ongoing'
    FINISHED = 'finished'
    ABANDONED = 'abandoned'


class Game(models.Model):
    """
    Describes a Dixit game.

    All games have an owner and are created as new. When a game is created
    the owner is added as a player and a new round recorded.

    A Game is `new` when the first round has not started yet. Once it starts
    it changes to `ongoing`. When a player wins it's changed to `finished`, if
    all players but one quit before the game is over, it's marked as `abandoned`
    """

    name = models.CharField(max_length=64)
    status = models.CharField(max_length=16, default='new', choices=GameStatus.choices())
    created_on = models.DateTimeField(auto_now_add=True)
    current_round = models.ForeignKey('Round', null=True, related_name='current_round')

    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')

        ordering = ('-created_on', )

    def update_status(self):
        """
        Game status is computed based on its Players and Round statuses.
        It is updated via a signal each time these change.

        The possible statuses are:
            - new: the game has no rounds, or it's only round is `new`
            - ongoing: the game play has a round in `providing` or `voting`
            - finished: all game rounds are `complete`
            - abandoned: all players have left the game
        """
        from dixit.game.models.round import Round, RoundStatus

        def all_rounds_complete():
            return all(r.status == RoundStatus.COMPLETE for r in self.rounds.all())

        if (self.rounds.count() == 0 or
            not self.current_round or
            self.current_round.number == 0 and self.current_round.status == RoundStatus.NEW):
            status = GameStatus.NEW

        elif self.players.count() == 0:
            status = GameStatus.ABANDONED

        elif all_rounds_complete():
            status = GameStatus.FINISHED

        else:
            status = GameStatus.ONGOING

        if self.status != status:
            self.status = status
            return self.save(update_fields=('status', ))

    def __str__(self):
        return self.name

    @property
    def storyteller(self):
        """
        Storyteller of the current round
        """
        return self.current_round.turn

    @classmethod
    def new_game(cls, name, user, player_name):
        """
        Bootstraps a new game with a round and a storyteller player
        """
        from dixit.game.models import Player, Round

        game = cls.objects.create(name=name)
        player = Player.objects.create(game=game, user=user, name=player_name, owner=True)

        game.add_round()
        return game

    def is_complete(self):
        """
        Checks if after the completion of the current round any player has achieved
        the goal score.
        """
        if (not self.current_round or
            self.current_round.status != RoundStatus.COMPLETE):
            return False

        for player in self.game.players():
            if player.score >= settings.GAME_GOAL_SCORE:
                return True

        return False

    def add_player(self, user, player_name):
        """
        Adds a new player to the game and deals cards if a round is available
        """
        from dixit.game.models import Player
        from dixit.game.models.round import RoundStatus

        player = Player.objects.create(game=self, user=user, name=player_name)
        playable_status = (RoundStatus.NEW, RoundStatus.PROVIDING)

        if self.current_round and self.current_round.status in playable_status:
            self.current_round.n_players += 1
            self.current_round.save(update_fields=('n_players', ))
            self.current_round.deal()

        return player

    def add_round(self):
        """
        Adds a new round to the game for the next player's turn
        """
        from dixit.game.models import Player, Round

        n_players = self.players.count()
        if n_players == 0:
            return None

        if not self.current_round:
            number, turn = 0, 0
        else:
            number = self.current_round.number + 1
            turn = (self.current_round.turn.number + 1) % n_players

        player = Player.objects.get(game=self, number=turn)
        game_round = Round(game=self, number=number, turn=player, n_players=n_players)

        # We need to assign the round first and save second
        # since the post-save signal will run on game and current_round needs to be set.
        # Since a model can't be saved with unsaved related object, this is the only order possible
        game_round.save()
        self.current_round = game_round
        self.save()
        game_round.deal()

        return game_round

    def update_turn(self, from_player):
        players = self.players.all().order_by('number')
        if not players:
            return

        for turn, p in enumerate(players):
            if p.number != turn:
                p.number = turn
                p.save()

        self.current_round.n_players = len(players)
        turn = (from_player.number + 1) % len(players)
        if not self.current_round.turn:
            self.current_round.turn = turn
            self.current_round.save(update_fields=('turn', 'n_players'))

    def next_round(self):
        """
        Closes the current round, which updates the scoring, and adds a new round.
        """
        self.current_round.close()
        if self.is_complete():
            raise GameFinished
        return self.add_round()


@receiver(post_save, sender='game.Round')
@receiver(post_delete, sender='game.Player')
def update_game_status(sender, instance, *args, **kwargs):
    return instance.game.update_status()
