
from rest_framework import serializers

from dixit.game.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializes Player objects
    """

    class Meta:
        model = Player
        fields = ('id', 'name', 'score', 'number')


class PlayerCreateSerializer(serializers.Serializer):
    """
    Serializes input for a Player object
    """
    name = serializers.CharField(max_length=64)


class PlayerScoreSerializer(serializers.ModelSerializer):
    """
    Serializers Player scores
    """

    class Meta:
        model = Player
        fields = ('name', 'score', )
