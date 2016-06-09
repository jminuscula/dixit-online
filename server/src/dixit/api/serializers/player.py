
from rest_framework import serializers

from dixit.game.models import Player


class PlayerScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'score', )


class PlayerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'score', 'order')
