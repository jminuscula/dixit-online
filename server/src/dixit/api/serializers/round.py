
import random
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from dixit.game.models import Game, Round, Player, Play, Card
from dixit.game.models.round import RoundStatus
from dixit.api.serializers.player import PlayerSerializer
from dixit.api.serializers.card import CardAnonymousSerializer


class RoundListSerializer(serializers.ModelSerializer):
    """
    Serializes a Round object in list mode
    """
    turn = PlayerSerializer(read_only=True)

    class Meta:
        model = Round
        fields = ('id', 'number', 'turn', 'status', )


class RoundRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializes a Round object in detail
      - Cards Provided won't be available until all round cards have been provided
    """
    turn = PlayerSerializer(read_only=True)
    story = serializers.SerializerMethodField()
    played_cards = serializers.SerializerMethodField()

    def get_story(self, game_round):
        try:
            storyteller_play = game_round.plays.get(player=game_round.turn)
        except ObjectDoesNotExist:
            return None
        return storyteller_play.story

    def get_played_cards(self, game_round):
        # played cards are only available once all players have chosen
        if game_round.status == RoundStatus.NEW or game_round.plays.count() < game_round.n_players:
            return []

        cards_provided = [play.card_provided for play in game_round.plays.all()]
        cards_provided.append(game_round.card)
        random.shuffle(cards_provided)
        return CardAnonymousSerializer(cards_provided, many=True).data

    class Meta:
        model = Round
        fields = ('id', 'number', 'turn', 'status', 'story', 'played_cards')



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
    Serializes input for a Play action, both provide/vote
    """
    story = serializers.CharField(max_length=256, required=False)
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all())
