
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from dixit.game.models import Game
from dixit.api.game.serializers.game import GameListSerializer
from dixit.api.auth.serializers.user import UserSerializer


class Me(generics.RetrieveAPIView):
    """
    Retrieves currently logged user info
    """

    model = User
    serializer_class = UserSerializer

    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UserGames(generics.ListAPIView):
    """
    Retrieves games where the user is or has participated
    """

    serializer_class = GameListSerializer

    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        qs = Game.objects.filter(players__user=self.request.user)
        status = self.request.query_params.get('status', None)
        if status is not None:
            return qs.filter(status=status)
        return qs
