
from django.test import TestCase
from django.contrib.auth.models import User

from dixit import settings
from dixit.game.models.game import Game, GameStatus
from dixit.game.models.player import Player


class PlayerTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@localhost', password='test')
        self.game = Game.objects.create(name='test')

    def test_player_generates_token_on_save(self):
        player = Player.objects.create(user=self.user, game=self.game)
        self.assertTrue(type(player.token) is bytes)
        self.assertEqual(len(player.token), settings.TOKEN_LENGTH * 2)

    def test_player_order_is_number_of_players(self):
        player = Player.objects.create(game=self.game, user=self.user, name='player1')
        self.assertEqual(player.number, 0)

        player = Player.objects.create(game=self.game, user=self.user, name='player2')
        self.assertEqual(player.number, 1)
