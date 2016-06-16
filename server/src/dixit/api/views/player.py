
from django.http import Http404
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from dixit.game.models import Player, Game
from dixit.api.serializers.player import PlayerSerializer, PlayerCreateSerializer, PlayerScoreSerializer


class PlayerList(generics.ListCreateAPIView):

    model = Player
    serializer_class = PlayerSerializer

    def _get_game(self):
        return get_object_or_404(Game, pk=self.kwargs['game_pk'])

    def get_queryset(self):
        return Player.objects.filter(game=self._get_game())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlayerCreateSerializer
        return PlayerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        game = self._get_game()
        try:
            player = game.add_player(request.data['name'])
        except IntegrityError:
            return Response({"name": ["Username already in use"]}, status=status.HTTP_403_FORBIDDEN)

        data = PlayerSerializer(player).data
        return Response(data, status=status.HTTP_201_CREATED)


class PlayerRetrieve(generics.RetrieveDestroyAPIView):

    model = Player
    serializer_class = PlayerSerializer

    def get_object(self):
        game_pk = self.kwargs['game_pk']
        number = self.kwargs['player_number']
        return get_object_or_404(Player, game=game_pk, number=number)
