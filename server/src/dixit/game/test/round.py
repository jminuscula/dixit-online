
from django.test import TestCase
from django.contrib.auth.models import User

from dixit import settings
from dixit.game.models.game import Game
from dixit.game.models.player import Player
from dixit.game.models.round import Round, RoundStatus, Play
from dixit.game.models.card import Card
from dixit.game.exceptions import GameInvalidPlay, GameRoundIncomplete, GameDeckExhausted


class PlayTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@localhost', password='test')
        self.user2 = User.objects.create(username='test2', email='test2@localhost', password='test')

        self.game = Game.new_game(name='test', user=self.user, player_name='storyteller')
        self.current = self.game.current_round
        self.player2 = self.game.add_player(self.user2, 'player2')

    def test_play_can_be_performed_for_round(self):
        story_card = self.game.storyteller._pick_card()
        Play.play_for_round(self.current, self.game.storyteller, story_card, 'story')
        self.assertEqual(self.current.plays.count(), 1)

    def test_storyteller_can_provide_card(self):
        story_play = Play(game_round=self.current, player=self.game.storyteller)
        story_play.provide_card(self.game.storyteller._pick_card(), 'story')
        self.assertEqual(self.current.plays.count(), 1)

    def test_players_cant_provide_card_before_storyteller(self):
        with self.assertRaises(GameInvalidPlay):
            Play.play_for_round(self.current, self.player2, self.player2._pick_card())

    def test_players_can_provide_card_after_storyteller(self):
        Play.play_for_round(self.current, self.game.storyteller, self.game.storyteller._pick_card(), 'story')
        Play.play_for_round(self.current, self.player2, self.player2._pick_card())
        self.assertEqual(self.current.plays.count(), 2)

    def test_players_can_not_provide_card_after_voting(self):
        # TODO
        pass

    def test_players_can_choose_played_card(self):
        story_card = self.game.storyteller._pick_card()
        story_play = Play.play_for_round(self.current, self.game.storyteller, story_card, 'story')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.current, self.player2, card2)
        play2.choose_card(story_card)

    def test_players_can_not_choose_unplayed_card(self):
        story_card = self.game.storyteller._pick_card()
        story_play = Play.play_for_round(self.current, self.game.storyteller, story_card, 'story')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.current, self.player2, card2)

        with self.assertRaises(GameInvalidPlay):
            other_card = Card.objects.available_for_game(self.game)[0]
            play2.choose_card(other_card)

    def test_players_can_not_choose_own_card(self):
        story_card = self.game.storyteller._pick_card()
        story_play = Play.play_for_round(self.current, self.game.storyteller, story_card, 'story')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.current, self.player2, card2)
        with self.assertRaises(GameInvalidPlay):
            play2.choose_card(card2)

    def test_storytellers_cant_choose_card(self):
        story_card = self.game.storyteller._pick_card()
        story_play = Play.play_for_round(self.current, self.game.storyteller, story_card, 'story')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.current, self.player2, card2)

        with self.assertRaises(GameInvalidPlay):
            story_play.choose_card(card2)


class RoundTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@localhost', password='test')
        self.user2 = User.objects.create(username='test2', email='test2@localhost', password='test')
        self.user3 = User.objects.create(username='test3', email='test3@localhost', password='test')
        self.user4 = User.objects.create(username='test4', email='test4@localhost', password='test')

        self.game = Game.new_game(name='test', user=self.user, player_name='storyteller')
        self.current = self.game.current_round
        self.player2 = self.game.add_player(self.user2, 'player2')
        self.player3 = self.game.add_player(self.user3, 'player3')

    def test_round_starts_new(self):
        self.assertEqual(self.current.status, RoundStatus.NEW)

    def test_round_is_pending_when_a_play_is_performed(self):
        story_card = self.game.storyteller._pick_card()
        Play.play_for_round(self.current, self.game.storyteller, story_card, 'story')
        self.assertEqual(self.current.status, RoundStatus.PENDING)

    def test_round_is_complete_when_all_plays_are_performed(self):
        story_card = self.game.storyteller._pick_card()
        Play.play_for_round(self.current, self.game.storyteller, story_card, 'story')

        players = self.game.players.all().exclude(id=self.game.storyteller.id)

        for player in players:
            Play.play_for_round(self.current, player, player._pick_card())

        plays = self.current.plays.all().exclude(player=self.game.storyteller)
        for play in plays:
            play.choose_card(story_card)

        self.assertEqual(self.current.status, RoundStatus.COMPLETE)

    def test_round_deals_hands_once_to_players(self):
        game_round = Round(game=self.game, number=self.current.number + 1, turn=self.current.turn)
        game_round.deal()
        game_round.deal()
        game_round.deal()

        hand_sizes = (p.cards.count() for p in self.game.players.all())
        self.assertTrue(all(s == settings.GAME_HAND_SIZE for s in hand_sizes))

    def test_round_deals_system_card(self):
        game_round = Round(game=self.game, number=self.current.number + 1, turn=self.current.turn)
        game_round.deal()
        self.assertTrue(game_round.card is not None)

    def test_round_deals_system_card_once(self):
        game_round = Round(game=self.game, number=self.current.number + 1, turn=self.current.turn)
        game_round.deal()

        system_card = game_round.card
        game_round.deal()
        self.assertEqual(system_card, game_round.card)

    def test_deal_fails_when_not_enough_cards_available(self):
        max_players = Card.objects.count() // (settings.GAME_HAND_SIZE + 1)

        for i in range(max_players + 1):
            test_username = 'test_n_{}'.format(i)
            test_email = '{}@localhost'.format(test_username)
            user = User.objects.create(username=test_username, email=test_email, password='test')
            Player.objects.create(game=self.game, user=user, name='player_{}'.format(i))

        new_round = Round(game=self.game, number=self.current.number + 1, turn=self.current.turn)
        with self.assertRaises(GameDeckExhausted):
            new_round.deal()

    def test_incomplete_round_can_not_be_closed(self):
        self.assertEqual(self.current.status, RoundStatus.NEW)
        self.assertRaises(GameRoundIncomplete, self.current.close)

        story_card = self.current.turn._pick_card()
        story_play = Play.play_for_round(self.current, self.current.turn, story_card, 'test')
        self.assertEqual(self.current.status, RoundStatus.PENDING)
        self.assertRaises(GameRoundIncomplete, self.current.close)

    def test_storyteller_scores_when_player_guessed(self):
        story_card = self.current.turn._pick_card()
        story_play = Play.play_for_round(self.current, self.current.turn, story_card, 'test')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.current, self.player2, card2)

        card3 = self.player3._pick_card()
        play3 = Play.play_for_round(self.current, self.player3, card3)

        play2.choose_card(story_card)
        play3.choose_card(card2)

        self.current.close()

        self.current.turn.refresh_from_db()
        self.assertEqual(self.current.turn.score, settings.GAME_STORY_SCORE)

    def test_storyteller_doesnt_score_when_all_players_guess(self):
        story_card = self.current.turn._pick_card()
        story_play = Play.play_for_round(self.current, self.current.turn, story_card, 'test')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.current, self.player2, card2)

        card3 = self.player3._pick_card()
        play3 = Play.play_for_round(self.current, self.player3, card3)

        play2.choose_card(story_card)
        play3.choose_card(story_card)

        self.current.close()

        self.current.turn.refresh_from_db()
        self.assertEqual(self.current.turn.score, 0)

    def test_players_score_when_their_card_is_chosen(self):
        story_card = self.current.turn._pick_card()
        story_play = Play.play_for_round(self.current, self.current.turn, story_card, 'test')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.current, self.player2, card2)

        card3 = self.player3._pick_card()
        play3 = Play.play_for_round(self.current, self.player3, card3)

        play2.choose_card(card3)
        play3.choose_card(card2)

        self.current.close()

        self.player2.refresh_from_db()
        self.assertEqual(self.player2.score, settings.GAME_CONFUSED_GUESS_SCORE)

    def test_players_score_max_bound(self):
        player4 = self.game.add_player(self.user4, 'player4')

        story_card = self.current.turn._pick_card()
        story_play = Play.play_for_round(self.current, self.current.turn, story_card, 'test')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.current, self.player2, card2)

        card3 = self.player3._pick_card()
        play3 = Play.play_for_round(self.current, self.player3, card3)

        card4 = player4._pick_card()
        play4 = Play.play_for_round(self.current, player4, card4)

        play2.choose_card(story_card)
        play3.choose_card(card2)
        play4.choose_card(card2)

        self.current.close()

        self.player2.refresh_from_db()
        self.assertEqual(self.player2.score, settings.GAME_MAX_ROUND_SCORE)
