
from django.shortcuts import get_object_or_404

from dixit.game.models import Game, Round


class GameObjectMixin:

    def get_game(self):
        return get_object_or_404(Game, pk=self.kwargs['game_pk'])


class RoundObjectMixin(GameObjectMixin):

    def get_round(self):
        game = self.get_game()
        round_number = self.kwargs['round_number']
        return get_object_or_404(Round, game=game, number=round_number)
