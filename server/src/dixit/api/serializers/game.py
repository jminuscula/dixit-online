
from rest_framework import serializers

from dixit.game.models import Game
from dixit.api.serializers.round import RoundListSerializer
from dixit.api.serializers.player import PlayerScoreSerializer


class GameBaseSerializer(serializers.HyperlinkedModelSerializer):
    """
    Base serializer for Game objects.
    """

    current_round = serializers.SerializerMethodField()
    def get_current_round(self, game):
        return RoundListSerializer(game.current_round).data

    scoreboard = serializers.SerializerMethodField()
    def get_scoreboard(self, game):
        return PlayerScoreSerializer(list(game.players.all()), many=True).data

    class Meta:
        model = Game


class GameListSerializer(GameBaseSerializer):
    """
    Serializes a Game object in list mode
    """
    n_players = serializers.SerializerMethodField()
    def get_n_players(self, game):
        return game.players.count()

    class Meta(GameBaseSerializer.Meta):
        model = Game
        fields = ('id', 'name', 'status', 'n_players', 'current_round', )


class GameCreateSerializer(serializers.Serializer):
    """
    Serializes the input for a new game
    """
    name = serializers.CharField(max_length=64)
    player_name = serializers.CharField(max_length=64)


class GameRetrieveSerializer(GameBaseSerializer):
    """
    Serializes a Game object with its full data
    """
    rounds = RoundListSerializer(many=True, read_only=True)

    class Meta(GameBaseSerializer.Meta):
        fields = ('id', 'name', 'status', 'rounds', 'scoreboard', )
        read_only_fields = ('status', )
