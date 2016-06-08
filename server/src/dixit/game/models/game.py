
from django.db import models
from django.utils.translation import ugettext as _


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

    def __str__(self):
        return self.name

    @classmethod
    def new_game(cls, name, player_name):
        """
        Bootstraps a new game with a round and a storyteller player
        """
        game = cls(name=name).save()
        player = Player(game=game, name=player_name, owner=True).save()
        game_round = Round(game=game, number=0, turn=player).save()
        game_round.deal()

        return game

    def cards_available(self):
        """
        Returns the cards remaining in the game deck
        """

    def scoreboard(self):
        return {p.id: p.score for p in self.players.all()}

    @property
    def current_round(self):
        rounds = self.rounds.all().order_by('-number')
        if rounds:
            return rounds[0]
        raise AttributeError('Game does not have any rounds yet')
