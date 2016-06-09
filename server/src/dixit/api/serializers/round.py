
from rest_framework import serializers

from dixit.game.models import Round
from dixit.api.serializers.fields import StatusField
from dixit.api.serializers.player import PlayerSerializer


class RoundListSerializer(serializers.ModelSerializer):
    """
    Serializes a Round object in list mode
    """
    status = StatusField(read_only=True)
    turn = PlayerSerializer(read_only=True)

    class Meta:
        model = Round
        fields = ('id', 'number', 'turn', 'status', )
