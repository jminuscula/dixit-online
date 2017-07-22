
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status

from dixit.game.models import Game
from dixit.game.exceptions import GameDeckExhausted
from dixit.api.game.serializers.game import GameListSerializer, GameCreateSerializer, GameRetrieveSerializer


class GameList(generics.ListCreateAPIView):
    """
    Implements Game list actions
        - GET list of games
        - POST a new game from game and player names
    """
    model = Game
    lookup_url_kwarg = 'game_pk'

    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GameCreateSerializer
        return GameListSerializer

    def get_queryset(self):
        qs = Game.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None:
            return qs.filter(status=status)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            game_name = serializer.validated_data['name']
            player_name = serializer.validated_data['player_name']
            game = Game.new_game(name=game_name, user=request.user, player_name=player_name)
        except GameDeckExhausted as exc:
            return Response({'detail': exc.msg}, status=status.HTTP_403_FORBIDDEN)
        data = GameRetrieveSerializer(game).data
        return Response(data, status=status.HTTP_201_CREATED)


class GameRetrieve(generics.RetrieveAPIView):
    """
    Implements Game retrieve actions
        - GET game details
    """

    serializer_class = GameRetrieveSerializer
    queryset = Game.objects.all()
    lookup_url_kwarg = 'game_pk'

    permission_classes = (IsAuthenticated, )
