
from django.test import TestCase
from django.contrib.auth.models import User

from dixit import settings
from dixit.game.models.game import Game, GameStatus
from dixit.game.models.round import Play
from dixit.game.models.card import Card
from dixit.game.exceptions import GameDeckExhausted, GameRoundIncomplete


class GameTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.game = Game.objects.create(name='test')
        self.user = User.objects.create(username='test', email='test@localhost', password='test')
        self.user2 = User.objects.create(username='test2', email='test2@localhost', password='test')

    def test_game_can_add_player(self):
        self.assertEqual(self.game.players.count(), 0)

        player_name = 'storyteller'
        self.game.add_player(self.user, player_name)
        self.assertEqual(self.game.players.count(), 1)
        self.assertEqual(self.game.players.all()[0].name, player_name)

    def test_game_cant_add_round_without_player(self):
        self.assertTrue(self.game.current_round is None)

        game_round = self.game.add_round()
        self.assertTrue(game_round is None)
        self.assertTrue(self.game.current_round is None)

    def test_game_can_add_round_if_player_present(self):
        self.game.add_player(self.user, 'storyteller')
        self.game.add_round()

        self.assertEqual(self.game.rounds.count(), 1)
        self.assertTrue(self.game.current_round is not None)

    def test_game_doesnt_add_round_if_no_cards_available(self):
        ncards = Card.objects.count()
        nplayers = (ncards // settings.GAME_HAND_SIZE) + 1

        for i in range(nplayers):
            test_username = 'test_n_{}'.format(i)
            test_email = '{}@localhost'.format(test_username)
            user = User.objects.create(username=test_username, email=test_email, password='test')
            self.game.add_player(user, 'player{}'.format(i))

        with self.assertRaises(GameDeckExhausted):
            self.game.add_round()
            self.assertEqual(self.game.rounds.count(), 0)
            self.assertTrue(self.game.current_round is None)

    def test_game_deals_new_player_when_round_is_added(self):
        storyteller = self.game.add_player(self.user, 'storyteller')
        self.assertEqual(storyteller.cards.count(), 0)

        self.game.add_round()
        self.assertEqual(storyteller.cards.count(), settings.GAME_HAND_SIZE)

    def test_game_deals_new_player_when_round_is_new(self):
        self.game.add_player(self.user, 'storyteller')
        self.game.add_round()

        player2 = self.game.add_player(self.user, 'player2')
        self.assertEqual(player2.cards.count(), settings.GAME_HAND_SIZE)

    def test_game_doesnt_deal_new_player_when_round_is_not_new(self):
        storyteller = self.game.add_player(self.user, 'storyteller')
        game_round = self.game.add_round()
        Play.play_for_round(game_round, storyteller, storyteller._pick_card(), 'test')

        player2 = self.game.add_player(self.user2, 'player2')
        self.assertEqual(player2.cards.count(), 0)

    def test_game_can_not_advance_round_when_previous_is_not_complete(self):
        storyteller = self.game.add_player(self.user, 'storyteller')
        game_round = self.game.add_round()
        Play.play_for_round(game_round, storyteller, storyteller._pick_card(), 'test')

        next_round = self.game.next_round()
        self.assertTrue(next_round is None)
        self.assertEqual(self.game.rounds.count(), 1)

    def test_game_can_advance_round_when_previous_is_complete(self):
        storyteller = self.game.add_player(self.user, 'storyteller')
        player2 = self.game.add_player(self.user2, 'player2')
        game_round = self.game.add_round()

        story_card = storyteller._pick_card()
        Play.play_for_round(game_round, storyteller, story_card, 'test')

        play2 = Play.play_for_round(game_round, player2, player2._pick_card())
        play2.choose_card(story_card)

        next_round = self.game.next_round()
        self.assertTrue(next_round is not None)
        self.assertEqual(self.game.rounds.count(), 2)

    def test_game_with_new_round_is_new(self):
        self.game.add_player(self.user, 'storyteller')
        self.game.add_round()

        self.assertEqual(self.game.status, GameStatus.NEW)

    def test_game_with_pending_round_is_ongoing(self):
        storyteller = self.game.add_player(self.user, 'storyteller')
        game_round = self.game.add_round()
        Play.play_for_round(game_round, storyteller, storyteller._pick_card(), 'test')

        self.assertEqual(self.game.status, GameStatus.ONGOING)

    def test_game_with_complete_round_is_finished(self):
        storyteller = self.game.add_player(self.user, 'storyteller')
        player2 = self.game.add_player(self.user2, 'player2')
        game_round = self.game.add_round()

        story_card = storyteller._pick_card()
        play1 = Play.play_for_round(game_round, storyteller, story_card, 'test')

        card2 = player2._pick_card()
        play2 = Play.play_for_round(game_round, player2, card2)
        play2.choose_card(story_card)

        self.assertEqual(self.game.status, GameStatus.FINISHED)

    def test_new_game_is_new(self):
        g = Game(name='test')
        self.assertEqual(g.status, GameStatus.NEW)

    def test_started_game_without_players_is_abandoned(self):
        g = Game.new_game(name='test', user=self.user, player_name='storyteller')
        g.players.all().delete()
        self.assertEqual(g.status, GameStatus.ABANDONED)

    def test_bootstrapped_game_has_player_and_round(self):
        g = Game.new_game(name='test', user=self.user, player_name='storyteller')
        self.assertEqual(g.players.count(), 1)
        self.assertTrue(g.current_round is not None)

    def test_bootstrapped_game_is_new(self):
        g = Game.new_game(name='test', user=self.user, player_name='storyteller')
        self.assertEqual(g.status, GameStatus.NEW)
