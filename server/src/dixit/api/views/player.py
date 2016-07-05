
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, status

from dixit.game.models import Player, Game
from dixit.api.serializers.player import PlayerSerializer, PlayerCreateSerializer, PlayerScoreSerializer
from dixit.api.views.mixins import GameObjectMixin


class PlayerList(GameObjectMixin, generics.ListCreateAPIView):
    """
    Implements Player list actions
        - GET list of players for a game
        - POST a new player t oa game from a player name
    """
    model = Player
    serializer_class = PlayerSerializer

    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Player.objects.filter(game=self.get_game())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlayerCreateSerializer
        return PlayerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            game = self.get_game()
            player = game.add_player(request.user, request.data['name'])
        except IntegrityError as exc:
            if 'user_id' in str(exc):
                return Response({"detail": 'You are already playing this game'}, status=status.HTTP_403_FORBIDDEN)
            return Response({"detail": "Username already in use"}, status=status.HTTP_403_FORBIDDEN)

        data = PlayerSerializer(player).data
        return Response(data, status=status.HTTP_201_CREATED)


class PlayerRetrieve(generics.RetrieveDestroyAPIView):
    """
    Implements Player retrieve action
        - GET player for game
    """

    model = Player
    serializer_class = PlayerSerializer

    permission_classes = (IsAuthenticated, )

    def get_object(self):
        game_pk = self.kwargs['game_pk']
        number = self.kwargs['player_number']
        try:
            return get_object_or_404(Player, game=game_pk, number=number)
        except Player.DoesNotExist:
            raise NotFound('player not found')
