
from django.test import TestCase

from dixit import settings
from dixit.game.models.game import Game, GameStatus
from dixit.game.models.round import Play
from dixit.game.models.card import Card
from dixit.game.exceptions import GameRoundIncomplete


class RoundTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.game = Game.new_game(name='test', player_name='storyteller')
        self.game.add_player('player2')
        self.game.add_player('player3')
        self.game.add_player('player4')
