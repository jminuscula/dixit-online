
from django.test import TestCase

from dixit import settings
from dixit.game.models.game import Game, GameStatus
from dixit.game.models.player import Player


class PlayerTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.game = Game(name='test')
        self.game.save()

    def test_player_generates_token_on_save(self):
        player = Player(game=self.game)
        player.save()
        self.assertTrue(type(player.token) is bytes)
        self.assertEqual(len(player.token), settings.TOKEN_LENGTH * 2)

    def test_player_order_is_number_of_players(self):
        player = Player(game=self.game, name='player1')
        player.save()

        self.assertEqual(player.order, 0)

        player = Player(game=self.game, name='player2')
        player.save()

        self.assertEqual(player.order, 1)
