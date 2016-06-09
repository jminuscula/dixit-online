
from rest_framework import serializers

from dixit.game.models import Player


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'score', 'order')


class PlayerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)


class PlayerScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('name', 'score', )
