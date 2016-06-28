
from django.test import TestCase
from django.contrib.auth.models import User

from dixit import settings
from dixit.game.models.game import Game, GameStatus
from dixit.game.models.round import Play
from dixit.game.models.player import Player
from dixit.game.models.card import Card


class CardManagerTest(TestCase):
    fixtures = ['game_testcards.json', ]

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@localhost', password='test')
        self.game = Game.new_game(name='test', user=self.user, player_name='storyteller')
        self.player2 = self.game.add_player(self.user, 'player2')

    def test_can_identified_cards_played_in_a_round(self):
        story_card = self.game.storyteller._pick_card()
        story_play = Play.play_for_round(self.game.current_round, self.game.storyteller, story_card, 'story')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.game.current_round, self.player2, card2)

        round_cards = {self.game.current_round.card, story_card, card2}
        self.assertEqual(set(Card.objects.played_for_round(self.game.current_round)), round_cards)

    def test_can_identified_cards_chosen_in_a_round(self):
        story_card = self.game.storyteller._pick_card()
        story_play = Play.play_for_round(self.game.current_round, self.game.storyteller, story_card, 'story')

        card2 = self.player2._pick_card()
        play2 = Play.play_for_round(self.game.current_round, self.player2, card2)
        play2.choose_card(story_card)

        self.assertEqual(set(Card.objects.chosen_for_round(self.game.current_round)), {story_card, })



class CardTest(TestCase):
    # TODO
    pass


class CardDescriptionTest(TestCase):
    # TODO
    pass
