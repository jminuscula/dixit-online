
import random

from django.db import models
from django.utils.translation import ugettext as _

from dixit import settings
from dixit.game.models import Game, Card, Player
from dixit.game.exceptions import GameDeckExhausted


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
    card = models.ForeignKey(Card, null=True, related_name='system_round_play')

    class Meta:
        verbose_name = _('round')
        verbose_name_plural = _('round')

        ordering = ('number', )
        unique_together = (('game', 'number'))


    def __str__(self):
        return "{} ({} of game {})".format(self.id, self.number, self.game.id)

    def deal(self):
        """
        Provides the players with cards and chooses the system card for this round.

        Each player must always have `GAME_HAND_SIZE` cards available. Players always
        lose a single card per round, so no calculation should be necessary. However,
        this method allows us to deal the initial hand to all players.
        """
        cards_available = list(Card.objects.available_for_game(self.game))

        card_deals = { 'system': 1 if not self.card else 0 }
        current_players = self.game.players.all().select_related()
        for player in current_players:
            card_deals[player] = settings.GAME_HAND_SIZE - player.cards.count()

        cards_needed = sum(card_deals.values())
        if cards_needed > len(cards_available):
            raise GameDeckExhausted

        def get_choice(seq):
            idx = random.randint(0, len(seq) - 1)
            return seq.pop(idx)

        for player in current_players:
            cards = [get_choice(cards_available) for i in range(card_deals[player])]
            player.cards.add(*cards)

        if not self.card:
            self.card = get_choice(cards_available)
            return self.save()


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

    # card being played in phase 1
    card_provided = models.ForeignKey(Card, related_name='plays')
    story = models.CharField(max_length=256, null=True)

    # card voted in phase 2 (storyteller can't vote)
    card_chosen = models.ForeignKey(Card, null=True, related_name='chosen')

    class Meta:
        verbose_name = _('play')
        verbose_name_plural = _('play')

        order_with_respect_to = 'player'
        unique_together = (('game_round', 'player'))
