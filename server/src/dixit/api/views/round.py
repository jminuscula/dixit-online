
from django.http import Http404
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from dixit.game.models import Game, Round
from dixit.api.serializers.round import RoundListSerializer


class RoundList(generics.ListAPIView):

    model = Round
    serializer_class = RoundListSerializer

    def _get_game(self):
        return get_object_or_404(Game, pk=self.kwargs['game_pk'])

    def get_queryset(self):
        return Round.objects.filter(game=self._get_game())

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return PlayerCreateSerializer
    #     return PlayerSerializer
    #
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     game = self._get_game()
    #     try:
    #         player = game.add_player(request.data['name'])
    #     except IntegrityError:
    #         return Response({"name": ["Username already in use"]}, status=status.HTTP_403_FORBIDDEN)
    #
    #     data = PlayerSerializer(player).data
    #     return Response(data, status=status.HTTP_201_CREATED)


class RoundRetrieve(generics.RetrieveAPIView):

    model = Round
    serializer_class = RoundListSerializer
    lookup_url_kwarg = 'round_pk'

    def get_object(self):
        game_pk = self.kwargs['game_pk']
        number = self.kwargs['round_number']
        return get_object_or_404(Round, game=game_pk, number=number)
