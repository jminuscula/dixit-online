
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from dixit.game.models import Player
from dixit.api.serializers.player import PlayerSerializer, PlayerScoreSerializer


class PlayerList(generics.ListCreateAPIView):

    model = Player
    serializer_class = PlayerSerializer

    def get_queryset(self):
        game_pk = self.kwargs['game_pk']
        return Player.objects.filter(game=game_pk)


class PlayerRetrieve(generics.RetrieveDestroyAPIView):

    model = Player
    serializer_class = PlayerSerializer
    lookup_url_kwarg = 'player_pk'

    def get_object(self):
        game_pk = self.kwargs['game_pk']
        player_pk = self.kwargs['player_pk']
        return Player.objects.get(game=game_pk, pk=player_pk)
