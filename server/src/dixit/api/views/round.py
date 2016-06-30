
from django.http import Http404
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status

from dixit.game.models import Game, Round, Play, Player, Card
from dixit.game.exceptions import GameInvalidPlay
from dixit.api.views.mixins import GameObjectMixin, RoundObjectMixin
from dixit.api.serializers.round import RoundListSerializer, RoundRetrieveSerializer
from dixit.api.serializers.round import PlaySerializer, PlayCreateSerializer
from dixit.api.permissions import GamePlayer, PlayerOwned


class RoundList(GameObjectMixin, generics.ListAPIView):
    model = Round
    serializer_class = RoundListSerializer

    permission_classes = (IsAuthenticated, GamePlayer)

    def get_queryset(self):
        return Round.objects.filter(game=self.get_game())


class RoundRetrieve(generics.RetrieveAPIView):
    model = Round
    serializer_class = RoundRetrieveSerializer
    lookup_url_kwarg = 'round_pk'

    permission_classes = (IsAuthenticated, GamePlayer)

    def get_object(self):
        game_pk = self.kwargs['game_pk']
        number = self.kwargs['round_number']
        return get_object_or_404(Round, game=game_pk, number=number)


class PlayList(RoundObjectMixin, generics.ListCreateAPIView):
    model = Play

    permission_classes = (IsAuthenticated, GamePlayer, PlayerOwned)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlayCreateSerializer
        return PlaySerializer

    def get_queryset(self):
        return Play.objects.filter(game_round=self.get_round())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        game_round = self.get_round()
        player = Player.objects.get(game=game_round.game, user=request.user)
        card = serializer.validated_data.get('card')
        story = serializer.validated_data.get('story')

        try:
            play = Play.play_for_round(game_round, player, card, story)
        except GameInvalidPlay as exc:
            return Response({'detail': exc.msg}, status=status.HTTP_403_FORBIDDEN)

        play_data = PlaySerializer(play).data
        return Response(play_data, status=status.HTTP_201_CREATED)


class PlayRetrieve(generics.RetrieveAPIView):
    model = Play
    serializer_class = PlaySerializer
    lookup_url_kwarg = 'play_pk'

    permission_classes = (IsAuthenticated, GamePlayer, PlayerOwned)

    def get_object(self):
        game_pk = self.kwargs['game_pk']
        round_number = self.kwargs['round_number']
        return get_object_or_404(Play, game=game_pk, round__number=round_number)
