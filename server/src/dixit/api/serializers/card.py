

from rest_framework import serializers

from dixit.game.models import Card


class CardAnonymousSerializer(serializers.ModelSerializer):

    def get_queryset(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()

    class Meta:
        model = Card
        field = ('name', 'path', )
