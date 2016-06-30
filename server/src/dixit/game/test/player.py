
from django.test import TestCase
from django.contrib.auth.models import User

from dixit import settings
from dixit.game.models.game import Game, GameStatus
from dixit.game.models.player import Player


class PlayerTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@localhost', password='test')
        self.user2 = User.objects.create(username='test2', email='test2@localhost', password='test2')
        self.game = Game.objects.create(name='test')

    def test_player_order_is_number_of_players(self):
        player = Player.objects.create(game=self.game, user=self.user, name='player1')
        self.assertEqual(player.number, 0)

        player = Player.objects.create(game=self.game, user=self.user2, name='player2')
        self.assertEqual(player.number, 1)
