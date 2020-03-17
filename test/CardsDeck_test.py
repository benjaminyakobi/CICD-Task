import unittest
from unittest.mock import Mock, patch
from src.CardsDeck import CardsDeck

class CardsDeckTest(unittest.TestCase):
    @patch('src.CardsDeck.CardsDeck.get_new_unshuffled_deck')
    def test_get_new_unshuffled_card_deck(self, mock_get_new_unshuffled_card_deck):
        #simulated deck to test if the deck is correctly created
        new_deck = {
            "success": True,
            "deck_id": "111111111111",
            "shuffled": False,
            "remaining": 52
        }
        #mock init
        mock_get_new_unshuffled_card_deck.return_value.status_code = 200
        mock_get_new_unshuffled_card_deck.return_value.json.return_value = new_deck
        #expected creating new deck, status code 200 and deck success == True
        n = CardsDeck()
        response = n.get_new_unshuffled_deck()
        #assert
        assert response.status_code == 200
        #success of creation
        self.assertEqual(response.json()['success'], True)
        #success when cards == 52
        self.assertEqual(response.json()['remaining'], 52)

    def test_get_new_shuffled_deck(self):
        new_ush_deck = Mock(CardsDeck)
        new_ush_deck.get_new_unshuffled_deck.json.return_value = \
        {
            "success": True,
            "deck_id": "111111111111",
            "shuffled": True,
            "remaining": 52
        }

        self.assertEqual(new_ush_deck.get_new_unshuffled_deck.json.return_value['remaining'], 52)
        self.assertEqual(new_ush_deck.get_new_unshuffled_deck.json.return_value['shuffled'], True)

if __name__ == '__main__':
    unittest.main()
