
from collections import defaultdict

from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from dixit.game.exceptions import GameRoundIncomplete


class Game(models.Model):
    """
    Describes a Dixit game.

    All games have an owner and are created as new. When a game is created
    the owner is added as a player and a new round recorded.

    A Game is `new` when the first round has not started yet. Once it starts
    it changes to `ongoing`. When a player wins it's changed to `finished`, if
    all players but one quit before the game is over, it's marked as `abandoned`
    """

    STATUS = (
        ('new', 'new'),
        ('ongoing', 'ongoing'),
        ('finished', 'finished'),
        ('abandoned', 'abandoned')
    )

    status = models.CharField(max_length=64, choices=STATUS, default='new')
    name = models.CharField(max_length=64)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')

        ordering = ('-created_on', )


    @property
    def current_round(self):
        rounds = self.rounds.all().order_by('-number')
        if rounds:
            return rounds[0]
        return None

    def __str__(self):
        return self.name

    @property
    def storyteller(self):
        """
        Storyteller of the current round
        """
        return self.current_round.turn

    @classmethod
    def new_game(cls, name, player_name):
        """
        Bootstraps a new game with a round and a storyteller player
        """
        from dixit.game.models import Player, Round

        game = cls(name=name)
        game.save()

        player = Player(game=game, name=player_name, owner=True)
        player.save()

        game.add_round()
        return game

    def add_player(self, player_name):
        from dixit.game.models import Player

        order = self.players.count() + 1
        player = Player(game=self, name=player_name, order=order)
        player.save()

        self.current_round.deal()

        return player

    def add_round(self):
        """
        Adds a new round to the game for the next player's turn
        """
        from dixit.game.models import Player, Round

        if not self.current_round:
            number, turn = 0, 0
        else:
            number = self.current_round.number + 1
            turn = (self.current_round.turn.order + 1) % self.players.count()

        player = Player.objects.get(game=self, order=turn)
        game_round = Round(game=self, number=number, turn=player)
        game_round.save()
        game_round.deal()

        return game_round

    def complete_round(self):
        """
        Closes the current round and updates the scoring.
        A new round is added.
        """
        from dixit.game.models import Play

        game_round = self.current_round
        storyteller = self.storyteller

        try:
            story_play = Play.objects.get(game_round=game_round, player=storyteller)
            story_card = story_play.card_provided
        except ObjectDoesNotExist:
            raise GameRoundIncomplete('storyteller needs to choose a card')

        plays = Play.objects.filter(game_round=game_round)
        if not all(p.card_chosen for p in players_plays):
            raise GameRoundIncomplete('round has pending players')

        scores = defaultdict(lambda x: 0)
        guesses = {p.player: False for p in plays}

        for play in plays:
            if play.card_chosen == story_card:
                scores[play.player] += settings.GAME_GUESS_SCORE
                guesses[play.player] = True
            else:
                chosen_play = Play.objects.get(card=play.card_chosen, game_round=game_round)
                scores[chosen_play.player] += 1

        if not all(guesses.values()):
            scores[storyteller] = settings.GAME_STORY_SCORE

        for player, score in scores.items():
            player.score += min(GAME_MAX_ROUND_SCORE, score)
            player.save()

        return self.add_round()
