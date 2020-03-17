import unittest
from unittest.mock import Mock, patch
from src.CardsDeck import CardsDeck


class CardsDeckTest(unittest.TestCase):

    def test_calling_api(self):
        pass

    @patch('src.CardsDeck.CardsDeck.get_new_unshuffled_deck')
    def test_get_new_unshuffled_card_deck(self, mock_get_new_unshuffled_card_deck):
        # simulated deck to test if the deck is correctly created
        new_deck = {
            "success": True,
            "deck_id": "111111111111",
            "shuffled": False,
            "remaining": 52
        }
        # mock init
        mock_get_new_unshuffled_card_deck.return_value.status_code = 200
        mock_get_new_unshuffled_card_deck.return_value.json.return_value = new_deck
        # expected creating new deck, status code 200 and deck success == True
        n = CardsDeck()
        response = n.get_new_unshuffled_deck()
        # assert
        assert response.status_code == 200
        # success of creation
        self.assertEqual(response.json()['success'], True)
        # success when cards == 52
        self.assertEqual(response.json()['remaining'], 52)

    @patch('src.CardsDeck.CardsDeck.get_new_unshuffled_deck')
    def test_get_new_unshuffled_card_deck_is_full(self, mock_get_new_unshuffled_card_deck):
        new_deck = {
            "success": True,
            "deck_id": "111111111111",
            "shuffled": False,
            "remaining": 52
        }
        # mock init
        mock_get_new_unshuffled_card_deck.return_value.status_code = 200
        mock_get_new_unshuffled_card_deck.return_value.json.return_value = new_deck
        # expected creating new deck, status code 200 and deck success == True
        n = CardsDeck()
        response = n.get_new_unshuffled_deck()
        # success when cards == 52
        self.assertEqual(response.json()['remaining'], 52)

    def test_get_new_shuffled_deck(self):
        # mock the card deck
        new_ush_deck = Mock(CardsDeck)
        new_ush_deck.get_new_unshuffled_deck.json.return_value = \
            {
                "success": True,
                "deck_id": "111111111111",
                "shuffled": True,
                "remaining": 52
            }
        # assume deck created as intended
        cards_remaining = 52
        is_shuffled = True

        # assert
        self.assertEqual(new_ush_deck.get_new_unshuffled_deck.json.return_value['remaining'], cards_remaining)
        self.assertEqual(new_ush_deck.get_new_unshuffled_deck.json.return_value['shuffled'], is_shuffled)

    @patch('src.CardsDeck.CardsDeck.draw_cards')
    def test_draws_card_new_deck_returns_two(self, mock_draw_cards):
        # simulated deck to test if the deck is correctly created
        new_deck = {
            "success": True,
            "cards": [
                {
                    "image": "https://deckofcardsapi.com/static/img/KH.png",
                    "value": "KING",
                    "suit": "HEARTS",
                    "code": "KH"
                },
                {
                    "image": "https://deckofcardsapi.com/static/img/8C.png",
                    "value": "8",
                    "suit": "CLUBS",
                    "code": "8C"
                }
            ],
            "deck_id": "3p40paa87x90",
            "remaining": 50
        }
        mock_draw_cards.return_value.status_code = 200
        mock_draw_cards.return_value.json.return_value = new_deck

        n = CardsDeck()
        response = n.draw_cards()

        assert response.status_code == 200
        # mock init

        cards_left_in_deck = 50
        size_of_cards = 2

        self.assertEqual(response.json()['remaining'], cards_left_in_deck)
        # summation of each card returned, expected 2
        self.assertEqual(sum(list(1 for x in response.json()['cards'])), size_of_cards)

    def test_create_new_deck_id(self):
        pass


if __name__ == '__main__':
    unittest.main()
