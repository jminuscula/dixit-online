
from rest_framework import permissions

from dixit.game.models import Game, Player


class GamePlayer(permissions.BasePermission):
    """
    """

    message = "You must be playing this game"

    def has_permission(self, request, view):
        try:
            game_pk = view.kwargs['game_pk']
            return Game.objects.get(pk=game_pk, players__user=request.user)
        except Game.DoesNotExist:
            return False



class PlayerOwned(permissions.BasePermission):
    """
    """

    message = "This play does not belong to you"

    def has_object_permission(self, request, view, obj):
        return obj.player.user == request.user
