
from django.test import TestCase

from dixit import settings
from dixit.game.models.game import Game, GameStatus
from dixit.game.models.round import Play
from dixit.game.models.card import Card
from dixit.game.exceptions import GameRoundIncomplete


class GameTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.game = Game(name='test')
        self.game.save()

    def test_game_can_add_player(self):
        self.assertEqual(self.game.players.all().count(), 0)

        player_name = 'storyteller'
        self.game.add_player(player_name)
        self.assertEqual(self.game.players.all().count(), 1)
        self.assertEqual(self.game.players.all()[0].name, player_name)

    def test_game_cant_add_round_without_player(self):
        self.assertTrue(self.game.current_round is None)

        game_round = self.game.add_round()
        self.assertTrue(game_round is None)
        self.assertTrue(self.game.current_round is None)

    def test_game_can_add_round_if_player_present(self):
        self.game.add_player('storyteller')
        self.game.add_round()

        self.assertEqual(self.game.rounds.all().count(), 1)
        self.assertTrue(self.game.current_round is not None)

    def test_game_doesnt_add_round_if_no_cards_available(self):
        ncards = Card.objects.all().count()
        nplayers = (ncards // settings.GAME_HAND_SIZE) + 1

        for i in range(nplayers):
            self.game.add_player('player{}'.format(i))

        self.game.add_round()
        self.assertEqual(self.game.rounds.all().count(), 0)
        self.assertTrue(self.game.current_round is None)

    def test_game_deals_new_player_when_round_is_added(self):
        storyteller = self.game.add_player('storyteller')
        self.assertEqual(storyteller.cards.all().count(), 0)

        self.game.add_round()
        self.assertEqual(storyteller.cards.all().count(), settings.GAME_HAND_SIZE)

    def test_game_deals_new_player_when_round_is_new(self):
        self.game.add_player('storyteller')
        self.game.add_round()

        player2 = self.game.add_player('player2')
        self.assertEqual(player2.cards.all().count(), settings.GAME_HAND_SIZE)

    def test_game_doesnt_deal_new_player_when_round_is_not_new(self):
        storyteller = self.game.add_player('storyteller')
        game_round = self.game.add_round()
        Play.play_for_round(game_round, storyteller, storyteller._pick_card(), 'test')

        player2 = self.game.add_player('player2')
        self.assertEqual(player2.cards.all().count(), 0)

    def test_game_with_new_round_is_new(self):
        self.game.add_player('storyteller')
        self.game.add_round()

        self.assertEqual(self.game.status, GameStatus.NEW)

    def test_game_with_pending_round_is_ongoing(self):
        storyteller = self.game.add_player('storyteller')
        game_round = self.game.add_round()
        Play.play_for_round(game_round, storyteller, storyteller._pick_card(), 'test')

        self.assertEqual(self.game.status, GameStatus.ONGOING)

    def test_game_with_complete_round_is_finished(self):
        storyteller = self.game.add_player('storyteller')
        player2 = self.game.add_player('player2')
        game_round = self.game.add_round()

        story_card = storyteller._pick_card()
        play1 = Play.play_for_round(game_round, storyteller, story_card, 'test')

        card2 = player2._pick_card()
        play2 = Play.play_for_round(game_round, player2, card2)
        play2.choose_card(story_card)

        self.assertEqual(self.game.status, GameStatus.FINISHED)

    def test_game_without_players_is_abandoned(self):
        g = Game(name='test')
        self.assertEqual(g.status, GameStatus.ABANDONED)

    def test_game_raises_error_when_complete_pending_round(self):
        self.game.add_player('storyteller')
        self.game.add_round()
        self.assertRaises(GameRoundIncomplete, self.game.complete_round)

    def test_game_storyteller_scores_when_player_guessed(self):
        storyteller = self.game.add_player('storyteller')
        player2 = self.game.add_player('player2')
        player3 = self.game.add_player('player3')
        game_round = self.game.add_round()

        story_card = storyteller._pick_card()
        play1 = Play.play_for_round(game_round, storyteller, story_card, 'test')

        card2 = player2._pick_card()
        play2 = Play.play_for_round(game_round, player2, card2)

        card3 = player3._pick_card()
        play3 = Play.play_for_round(game_round, player3, card3)

        play2.choose_card(story_card)
        play3.choose_card(card2)

        self.game.complete_round()

        storyteller.refresh_from_db()
        self.assertEqual(storyteller.score, settings.GAME_STORY_SCORE)

    def test_game_storyteller_doesnt_score_when_all_players_guess(self):
        storyteller = self.game.add_player('storyteller')
        player2 = self.game.add_player('player2')
        player3 = self.game.add_player('player3')
        game_round = self.game.add_round()

        story_card = storyteller._pick_card()
        play1 = Play.play_for_round(game_round, storyteller, story_card, 'test')

        card2 = player2._pick_card()
        play2 = Play.play_for_round(game_round, player2, card2)

        card3 = player3._pick_card()
        play3 = Play.play_for_round(game_round, player3, card3)

        play2.choose_card(story_card)
        play3.choose_card(story_card)

        self.game.complete_round()

        storyteller.refresh_from_db()
        self.assertEqual(storyteller.score, 0)

    def test_game_players_score_when_their_card_is_chosen(self):
        storyteller = self.game.add_player('storyteller')
        player2 = self.game.add_player('player2')
        player3 = self.game.add_player('player3')
        game_round = self.game.add_round()

        story_card = storyteller._pick_card()
        play1 = Play.play_for_round(game_round, storyteller, story_card, 'test')

        card2 = player2._pick_card()
        play2 = Play.play_for_round(game_round, player2, card2)

        card3 = player3._pick_card()
        play3 = Play.play_for_round(game_round, player3, card3)

        play2.choose_card(card3)
        play3.choose_card(card2)

        self.game.complete_round()

        player2.refresh_from_db()
        self.assertEqual(player2.score, settings.GAME_CONFUSED_GUESS_SCORE)

    def test_game_players_score_max_bound(self):
        storyteller = self.game.add_player('storyteller')
        player2 = self.game.add_player('player2')
        player3 = self.game.add_player('player3')
        player4 = self.game.add_player('player4')
        game_round = self.game.add_round()

        story_card = storyteller._pick_card()
        play1 = Play.play_for_round(game_round, storyteller, story_card, 'test')

        card2 = player2._pick_card()
        play2 = Play.play_for_round(game_round, player2, card2)

        card3 = player3._pick_card()
        play3 = Play.play_for_round(game_round, player3, card3)

        card4 = player4._pick_card()
        play4 = Play.play_for_round(game_round, player4, card4)

        play2.choose_card(story_card)
        play3.choose_card(card2)
        play4.choose_card(card2)

        self.game.complete_round()

        player2.refresh_from_db()
        self.assertEqual(player2.score, settings.GAME_MAX_ROUND_SCORE)

    def test_bootstrapped_game_has_player_and_round(self):
        g = Game.new_game(name='test', player_name='storyteller')
        self.assertEqual(g.players.all().count(), 1)
        self.assertTrue(g.current_round is not None)

    def test_bootstrapped_game_is_new(self):
        g = Game.new_game(name='test', player_name='storyteller')
        self.assertEqual(g.status, GameStatus.NEW)
