
import enum
import random

from django.db import models
from django.utils.translation import ugettext as _

from dixit import settings
from dixit.game.models import Game, Card, CardDescription, Player
from dixit.game.exceptions import GameDeckExhausted, GameInvalidPlay


class RoundStatus(enum.Enum):
    NEW = 'new'
    PENDING = 'pending'
    COMPLETE = 'complete'


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

    game = models.ForeignKey(Game, related_name='rounds')
    number = models.IntegerField(default=0)
    turn = models.ForeignKey(Player)
    card = models.ForeignKey(Card, null=True, related_name='system_round_play')

    class Meta:
        verbose_name = _('round')
        verbose_name_plural = _('round')

        ordering = ('number', )
        unique_together = (('game', 'number'))


    def __str__(self):
        return "{} ({} of game {})".format(self.id, self.number, self.game.id)

    @property
    def status(self):
        plays = self.plays.all()

        if not plays:
            return RoundStatus.NEW

        # check if there are players pending
        # if storyteller is the only one who has played, the game is still ongoing
        # since other players may join the current round.
        play_status = {p.player: p.complete for p in plays}
        if not all(play_status.values()) or play_status.keys() == {self.turn}:
            return RoundStatus.PENDING

        return RoundStatus.COMPLETE

    def deal(self):
        """
        Provides the players with cards and chooses the system card for this round.

        Each player must always have `GAME_HAND_SIZE` cards available. Players always
        lose a single card per round, so no calculation should be necessary. However,
        this method allows us to deal the initial hand to all players.
        """
        cards_available = list(Card.objects.available_for_game(self.game))
        current_players = self.game.players.all().select_related()

        card_deals = {
            'system': 1 if not self.card else 0,
            # if the storyteller is the only one playing, we need to make sure we have
            # enough cards to deal a joining player.
            'player': settings.GAME_HAND_SIZE if current_players.count() == 1 else 0
        }

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
            # TODO
            # If the round dealt the system card after the storyteller had given the
            # description, a smarter choice could me made.
            self.card = get_choice(cards_available)
            return self.save()


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

    @property
    def complete(self):
        if self.player == self.game_round.turn:
            return self.card_provided is not None
        return self.card_chosen is not None

    @classmethod
    def play_for_round(cls, game_round, player, card, story=None):
        play = cls(game_round=game_round, player=player)
        return play.provide_card(card, story)

    def provide_card(self, card, story=None):
        """
        Play a card for the current round.
        Storytellers must provide a story when providing a card.
        """
        if story is None and self.player == self.game_round.turn:
            raise GameInvalidPlay('the storyteller needs to provide a story')

        self.card_provided = card
        self.save()

        return self

    def choose_card(self, card):
        """
        Choose a card among all provided in the round. The round must be complete.
        Players can't choose their own cards.
        """
        if self.player == self.game_round.turn:
            raise GameInvalidPlay('storytellers can not choose any cards')

        if card == self.card_provided:
            raise GameInvalidPlay('player can not choose their own card')

        round_cards = set(Card.objects.played_for_round(self.game_round))
        if len(round_cards) != self.game_round.game.players.count():
            raise GameInvalidPlay('not all players have provided a card yet')

        if card not in round_cards:
            raise GameInvalidPlay('the chosen card is not being played in this round')

        self.card_chosen = card
        self.save()

        return self
