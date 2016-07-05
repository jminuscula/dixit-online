

from rest_framework import serializers

from dixit.game.models import Card


class CardAnonymousSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        field = ('name', 'path', )
