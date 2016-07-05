
from rest_framework import permissions
from rest_framework.exceptions import NotFound

from dixit.game.models import Game, Player


class GamePlayer(permissions.BasePermission):
    """
    Checks current user is a player on the game related to the request object
    """

    message = "You must be playing this game"

    def has_permission(self, request, view):
        try:
            game_pk = view.kwargs['game_pk']
            return Game.objects.get(pk=game_pk, players__user=request.user)
        except Game.DoesNotExist:
            raise NotFound('game not found')



class PlayerOwned(permissions.BasePermission):
    """
    Checks current user is the player directly related to the request object
    """

    message = "This play does not belong to you"

    def has_object_permission(self, request, view, obj):
        return obj.player.user == request.user
