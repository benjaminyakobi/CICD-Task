import unittest
from unittest.mock import Mock, patch
from src.CardsDeck import CardsDeck

class CardsDeckTest(unittest.TestCase):
    @patch('src.CardsDeck.CardsDeck.getNewCardDeck')
    def test_get_new_card_deck(self, mock_get_new_card_deck):
        #simulated deck
        new_deck = {
            "success": True,
            "deck_id": "111111111111",
            "shuffled": True,
            "remaining": 52
        }
        #mock init
        mock_get_new_card_deck.return_value.status_code = 200
        mock_get_new_card_deck.return_value.json.return_value = new_deck
        #expected creating new deck, status code 200 and deck success == True
        n = CardsDeck()
        response = n.getNewCardDeck()
        #assert
        assert response.status_code == 200
        self.assertEqual(response.json()['success'], True)

if __name__ == '__main__':
    unittest.main()
