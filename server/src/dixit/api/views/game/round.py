
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, status

from dixit.game.models import Round, Play, Player
from dixit.game.models.round import RoundStatus
from dixit.game.exceptions import GameInvalidPlay, GameDeckExhausted, GameFinished
from dixit.api.views.game.mixins import GameObjectMixin, RoundObjectMixin
from dixit.api.serializers.round import RoundListSerializer, RoundRetrieveSerializer
from dixit.api.serializers.round import PlaySerializer, PlayCreateSerializer
from dixit.api.permissions import GamePlayer, PlayerOwned


class RoundList(GameObjectMixin, generics.ListAPIView):
    """
    Implements Round list actions
        - GET list of game rounds

    Rounds are managed by the game itself and can't be added from the API
    """
    model = Round
    serializer_class = RoundListSerializer

    permission_classes = (IsAuthenticated, GamePlayer)

    def get_queryset(self):
        return Round.objects.filter(game=self.get_game())


class RoundRetrieve(RoundObjectMixin, generics.RetrieveAPIView):
    """
    Implements Round retrieve actions
        - GET round details
    """
    model = Round
    serializer_class = RoundRetrieveSerializer
    lookup_url_kwarg = 'round_pk'

    permission_classes = (IsAuthenticated, GamePlayer)

    def get_object(self):
        return self.get_round()


class PlayList(RoundObjectMixin, generics.ListCreateAPIView):
    """
    Implements Play list actions
        - GET list of round plays

    Plays are created using two specific endpoints: Provide and Vote
    """
    model = Play
    permission_classes = (IsAuthenticated, GamePlayer)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlayCreateSerializer
        return PlaySerializer

    def get_queryset(self):
        return Play.objects.filter(game_round=self.get_round())


class PlayRetrieve(generics.RetrieveAPIView):
    """
    Implements Play retrieve actions
        - GET play details
    """
    model = Play
    serializer_class = PlaySerializer
    lookup_url_kwarg = 'play_pk'

    permission_classes = (IsAuthenticated, GamePlayer, PlayerOwned)

    def get_object(self):
        game_pk = self.kwargs['game_pk']
        round_number = self.kwargs['round_number']
        try:
            return Play.objects.get(game=game_pk, round__number=round_number)
        except Play.DoesNotExist:
            raise NotFound('play not found')


class PlayProvideCreate(RoundObjectMixin, generics.CreateAPIView):
    """
    Implements Play provide action
        - POST a new play providing a card

    POST may be called any number of times as long as the round is in PROVIDING state
    """
    model = Play
    serializer_class = PlayCreateSerializer
    permission_classes = (IsAuthenticated, GamePlayer)

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

class PlayVoteCreate(RoundObjectMixin, generics.CreateAPIView):
    """
    Implements Play vote action
        - POST a new vote

    POST may be called any number of times as long as the round is in VOTING state
    """
    model = Play
    serializer_class = PlayCreateSerializer
    permission_classes = (IsAuthenticated, GamePlayer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        game_round = self.get_round()
        player = Player.objects.get(game=game_round.game, user=request.user)
        card = serializer.validated_data.get('card')
        play = Play.objects.get(game_round=game_round, player=player)

        try:
            play.vote_card(card)
        except GameInvalidPlay as exc:
            return Response({'detail': exc.msg}, status=status.HTTP_403_FORBIDDEN)

        game_round.refresh_from_db()
        if game_round.status == RoundStatus.COMPLETE:
            game = self.get_game()
            try:
                game.next_round()
            except (GameDeckExhausted, GameFinished):  # treat deck exhaust as a fair finish
                pass

        play_data = PlaySerializer(play).data
        return Response(play_data, status=status.HTTP_201_CREATED)
