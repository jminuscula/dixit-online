
from django.db import models
from django.utils.translation import ugettext as _

from dixit import settings


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
