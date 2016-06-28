
from rest_framework import serializers

from dixit.game.models import Game, Round, Player, Play, Card
from dixit.api.serializers.player import PlayerSerializer


class RoundListSerializer(serializers.ModelSerializer):
    """
    Serializes a Round object in list mode
    """
    turn = PlayerSerializer(read_only=True)

    class Meta:
        model = Round
        fields = ('id', 'number', 'turn', 'status', )


class PlaySerializer(serializers.ModelSerializer):
    """
    Serializes a Play object
    """
    player = PlayerSerializer()

    class Meta:
        model = Play
        fields = ('id', 'player', 'story', )


class PlayCreateSerializer(serializers.Serializer):
    """
    """
    story = serializers.CharField(max_length=256, required=False)
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all())
