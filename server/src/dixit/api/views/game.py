
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from dixit.game.models import Game
from dixit.api.serializers.game import GameListSerializer, GameCreateSerializer, GameRetrieveSerializer
from dixit.api.serializers.round import RoundListSerializer


class GameList(generics.ListCreateAPIView):

    model = Game
    queryset = Game.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GameCreateSerializer
        return GameListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        game = Game.new_game(name=request.data['name'], player_name=request.data['player_name'])
        data = GameRetrieveSerializer(game).data
        return Response(data, status=status.HTTP_201_CREATED)


class GameRetrieve(generics.RetrieveAPIView):

    serializer_class = GameRetrieveSerializer
    queryset = Game.objects.all()
    lookup_url_kwarg = 'game_pk'
