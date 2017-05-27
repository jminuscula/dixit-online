
from rest_framework.exceptions import NotFound

from dixit.game.models import Game, Round


class GameObjectMixin:
    """
    Gets Game object for child endpoints
    """

    def get_game(self):
        try:
            return Game.objects.get(pk=self.kwargs['game_pk'])
        except Game.DoesNotExist:
            raise NotFound('game not found')


class RoundObjectMixin(GameObjectMixin):
    """
    Gets Round object for child endpoints
    """

    def get_round(self):
        try:
            game = self.get_game()
            round_number = self.kwargs['round_number']
            return Round.objects.get(game=game, number=round_number)
        except Game.DoesNotExist:
            raise NotFound('game not found')
        except Round.DoesNotExist:
            raise NotFound('round not found')
