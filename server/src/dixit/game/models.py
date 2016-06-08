
import os
import binascii

from django.db import models
from django.utils.translation import ugettext as _

from dixit import settings


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

    def scoreboard(self):
        return {p.id: p.score for p in self.players.all()}

    @property
    def current_round(self):
        rounds = self.rounds.all().order_by('-number')
        if rounds:
            return rounds[0]
        raise AttributeError('Game does not have any rounds yet')


class Card(models.Model):
    """
    Describes a playing Card.

    Players choose and vote these cards in each round.
    """
    path = models.FilePathField(settings.CARD_IMAGES_PATH)
    name = models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name = _('card')
        verbose_name_plural = _('cards')

    @classmethod
    def get_for_description(cls, description):
        pass


class CardDescription(models.Model):
    """
    Describes a playing card through the labels that different players have chosen
    for it over time. The description confidence depends on the level in which the
    description is provided.

    A description chosen for this card by the storyteller will have 100 confidence.
    Cards from other players that have been voted will also have this description
    attached, with a variable confidence depending on ratio of players who voted it.
    """
    card = models.ForeignKey(Card, related_name='description')
    description = models.CharField(max_length=256)
    confidence = models.IntegerField(default=50)

    class Meta:
        verbose_name = _('card description')
        verbose_name_plural = _('card descriptions')


class Player(models.Model):
    """
    Describes a player for a specific game.

    Players are handed a security token to perform actions in the game, such as
    playing a round or abandoning.
    """
    game = models.ForeignKey(Game, related_name='players')
    owner = models.BooleanField(default=False)
    name = models.CharField(max_length=64)
    token = models.CharField(max_length=64)
    score = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    cards = models.ManyToManyField(Card)

    class Meta:
        verbose_name = _('player')
        verbose_name_plural = _('player')

        ordering = ('order', )
        unique_together = (('game', 'name'), ('game', 'order'))

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(settings.TOKEN_LENGHT))

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = Player.generate_token()
        return super().save(*args, **kwargs)


class Round(models.Model):
    """
    Describes a game round.

    Games are composed of a series of ordered rounds, which define which player
    is the storyteller.

    A round is created `new` and transitions to `pending` once the storyteller has
    played. When all other players are done is marked as `complete`.

    Each round has a card that is taken from the pool to be played by the system,
    in order to confuse other players.
    """

    STATUS = (
        ('new', 'new'),
        ('pending', 'pending'),
        ('complete', 'complete'),
    )

    game = models.ForeignKey(Game, related_name='rounds')
    number = models.IntegerField(default=0)
    turn = models.ForeignKey(Player)
    complete = models.CharField(max_length=64, choices=STATUS, default='new')
    card = models.ForeignKey(Card)

    class Meta:
        verbose_name = _('round')
        verbose_name_plural = _('round')

        ordering = ('number', )
        unique_together = (('game', 'number'))

    def __str__(self):
        return "{} (Game {})".format(self.id, self.game.id)

    def get_system_card(self):
        pass


class Play(models.Model):
    """
    Describes a playing move for a player in a round.

    If the player is the storyteller a story must be provided and card_chosen won't
    be set. Otherwise, a story can't be provided.

    Note that a play covers both phases of each round -eg: providing a card and
    voting on all the available cards at the end of the round.
    """

    game_round = models.ForeignKey(Round, related_name='plays')
    player = models.ForeignKey(Player)
    card_provided = models.ForeignKey(Card, null=True, related_name='provided')
    card_chosen = models.ForeignKey(Card, null=True, related_name='chosen')
    story = models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name = _('play')
        verbose_name_plural = _('play')

        order_with_respect_to = 'player'
        unique_together = (('game_round', 'player'))
