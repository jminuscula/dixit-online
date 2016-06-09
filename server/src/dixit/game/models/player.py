
import os
import binascii

from django.db import models
from django.utils.translation import ugettext as _

from dixit import settings
from dixit.game.models import Game, Card


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
    order = models.IntegerField()
    cards = models.ManyToManyField(Card, related_name='played_by')

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
        if not self.order:
            self.order = self.game.players.count()
        return super().save(*args, **kwargs)

    def _pick_card(self):
        """
        helper method to ease testing.
        Returns the first card in the hand
        """
        hand = self.cards.all()
        if hand.count():
            return hand[0]
        return None
