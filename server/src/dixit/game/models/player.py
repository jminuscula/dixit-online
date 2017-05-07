
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from dixit.game.models import Game, Card


class Player(models.Model):
    """
    Describes a player for a specific game.

    Players are handed a security token to perform actions in the game, such as
    playing a round or abandoning.
    """
    user = models.ForeignKey(User, related_name='players', on_delete=models.PROTECT)
    game = models.ForeignKey(Game, related_name='players', on_delete=models.PROTECT)
    number = models.IntegerField(default=0)  # (game, number form pk together)
    owner = models.BooleanField(default=False)
    name = models.CharField(max_length=64, blank=False)
    token = models.CharField(max_length=64)
    score = models.IntegerField(default=0)
    cards = models.ManyToManyField(Card, related_name='played_by')

    class Meta:
        verbose_name = _('player')
        verbose_name_plural = _('player')

        ordering = ('number', )
        unique_together = (('game', 'user'), ('game', 'name'), ('game', 'number'))

    def __str__(self):
        return "{}, {} of <Game {}: '{}'>".format(self.name, self.number, self.game.id, self.game.name)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.game.players.count()
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
