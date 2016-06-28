
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _

from dixit import settings


class CardManager(models.Manager):

    def available_for_game(self, game):
        """
        Returns the cards remaining in the game deck
        """
        from dixit.game.models import Play

        game_rounds = game.rounds.all()
        plays = Play.objects.filter(game_round__in=game_rounds)

        played_cards = Q(plays__in=plays)
        dealt_cards = Q(played_by__in=game.players.all())
        system_cards = Q(system_round_play__in=game_rounds)

        return self.all().exclude(played_cards | dealt_cards | system_cards)

    def played_for_round(self, game_round):
        from dixit.game.models import Play

        plays = Play.objects.filter(game_round=game_round)
        return self.filter(Q(plays__in=plays) | Q(id=game_round.card.id))

    def chosen_for_round(self, game_round):
        from dixit.game.models import Play

        plays = Play.objects.filter(game_round=game_round)
        return self.filter(chosen__in=plays)


class Card(models.Model):
    """
    Describes a playing Card.

    Players choose and vote these cards in each round.
    """
    path = models.FilePathField(settings.CARD_IMAGES_PATH)
    name = models.CharField(max_length=256, null=True)

    objects = CardManager()

    class Meta:
        verbose_name = _('card')
        verbose_name_plural = _('cards')

    def __str__(self):
        return self.name or self.path

    @classmethod
    def get_for_description(cls, available, description):
        """
        Returns a card from the available deck based on the accuracy for the
        provided description.
        The card is removed from the deck.
        """
        # TODO


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
