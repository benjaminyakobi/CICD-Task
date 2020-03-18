import unittest
from unittest.mock import Mock, patch
import CardLogic
from requests.exceptions import Timeout
import requests

URL_NEW_PARTIAL_DECK = 'https://deckofcardsapi.com/api/deck/new/shuffle/?cards='
requests = Mock()

NEW_PARTIAL_DECK = {
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
NEW_DECK_SHUFFLED = {
    "success": True,
    "deck_id": "111111111111",
    "shuffled": True,
    "remaining": 52
}
NEW_DECK_UNSHUFFLED = {
    "success": True,
    "deck_id": "111111111111",
    "shuffled": False,
    "remaining": 52
}


def getpartial_deck(cards=None):
    # The value, one of A (for an ace), 2, 3, 4, 5, 6, 7, 8, 9, 0 (for a ten), J (jack), Q (queen), or K (king);
    # The suit, one of S (Spades), D (Diamonds), C (Clubs), or H (Hearts).
    r = requests.get(URL_NEW_PARTIAL_DECK + 'KH,AS')
    if r.status_code == 200:
        return r.json()
    return None


class CardsDeckTestCreation(unittest.TestCase):

    @patch('CardLogic.CardsDeck.get_new_unshuffled_deck')
    def test_get_new_unshuffled_card_deck(self, mock_get_new_unshuffled_card_deck):
        # mock init
        mock_get_new_unshuffled_card_deck.return_value.status_code = 200
        mock_get_new_unshuffled_card_deck.return_value.json.return_value = NEW_DECK_UNSHUFFLED
        # expected creating new deck, status code 200 and deck success == True
        n = CardLogic.CardsDeck()
        response = n.get_new_unshuffled_deck()
        # assert
        assert response.status_code == 200
        # success of creation
        self.assertEqual(response.json()['success'], True)
        # success when cards == 52
        self.assertEqual(response.json()['remaining'], 52)

    @patch('CardLogic.CardsDeck.get_new_unshuffled_deck')
    def test_get_new_unshuffled_card_deck_is_full(self, mock_get_new_unshuffled_card_deck):
        # mock init
        mock_get_new_unshuffled_card_deck.return_value.status_code = 200
        mock_get_new_unshuffled_card_deck.return_value.json.return_value = NEW_DECK_UNSHUFFLED
        # expected creating new deck, status code 200 and deck success == True
        n = CardLogic.CardsDeck()
        response = n.get_new_unshuffled_deck()
        # success when cards == 52
        self.assertEqual(response.json()['remaining'], 52)

    def test_get_new_shuffled_deck_expected_true(self):
        # mock the card deck
        new_ush_deck = Mock(CardLogic.CardsDeck)
        new_ush_deck.get_new_unshuffled_deck.json.return_value = NEW_DECK_SHUFFLED
        # assume deck created as intended
        cards_remaining = 52
        is_shuffled = True

        # assert
        self.assertEqual(new_ush_deck.get_new_unshuffled_deck.json.return_value['remaining'], cards_remaining)
        self.assertEqual(new_ush_deck.get_new_unshuffled_deck.json.return_value['shuffled'], is_shuffled)

    def test_get_new_shuffled_deck_expected_false(self):
        # mock the card deck
        new_ush_deck = Mock(CardLogic.CardsDeck)
        new_ush_deck.get_new_unshuffled_deck.json.return_value = NEW_DECK_UNSHUFFLED
        # assume deck created as intended
        cards_remaining = 52
        is_shuffled = True

        # assert
        self.assertEqual(new_ush_deck.get_new_unshuffled_deck.json.return_value['remaining'], cards_remaining)
        with self.assertRaises(AssertionError):
            self.assertEqual(new_ush_deck.get_new_unshuffled_deck.json.return_value['shuffled'], is_shuffled)

    @patch('CardLogic.CardsDeck.draw_cards')
    def test_draws_card_new_deck_returns_two(self, mock_draw_cards):
        # simulated deck to test if the deck is correctly created

        mock_draw_cards.return_value.status_code = 200
        mock_draw_cards.return_value.json.return_value = NEW_PARTIAL_DECK

        n = CardLogic.CardsDeck()
        response = n.draw_cards()

        assert response.status_code == 200
        # mock init

        cards_left_in_deck = 50
        size_of_cards = 2

        self.assertEqual(response.json()['remaining'], cards_left_in_deck)
        # summation of each card returned, expected 2
        self.assertEqual(sum(list(1 for x in response.json()['cards'])), size_of_cards)

    def test_get_response_succeeded(self):
        mocked_deck = CardLogic.CardsDeck()
        # mock CardsDeck.get_new_partial_deck
        mocked_deck.get_new_partial_deck = Mock()
        # load with incorrect url
        mocked_deck.get_new_partial_deck.loads('https://deckofcardsapi.com/api/deck/new/shuffle/?cards=AS')
        # expecting wrong url
        mocked_deck.get_new_partial_deck.loads.assert_called_with('{}'.format(URL_NEW_PARTIAL_DECK + 'AS'))

    def test_get_response_failed(self):
        mocked_deck = CardLogic.CardsDeck()
        # mock CardsDeck.get_new_partial_deck
        mocked_deck.get_new_partial_deck = Mock()
        # load with incorrect url
        mocked_deck.get_new_partial_deck.loads('https://deckofcardsapi.com/api/deck/new/shuffle/?cards=')
        # expecting wrong url
        mocked_deck.get_new_partial_deck.loads.assert_called_with('{}'.format(URL_NEW_PARTIAL_DECK))

    def test_create_new_deck_timeout_retry_pass(self):
        # imitating response
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = NEW_PARTIAL_DECK
        # set side effect of get
        requests.get.side_effect = [Timeout, response_mock]
        # first test raises timeout
        with self.assertRaises(Timeout):
            getpartial_deck()
        # retry for expected successful response
        assert getpartial_deck()['success'] == True
        # check that get was called twice
        assert requests.get.call_count == 2

    def test_two_new_decks_are_same(self):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = NEW_PARTIAL_DECK

        response_mock2 = Mock()
        response_mock2.status_code = 200
        response_mock2.json.return_value = NEW_PARTIAL_DECK
        # expected to be true
        self.assertEqual(response_mock.json()['deck_id'], response_mock2.json()['deck_id']) == True

    def test_two_new_decks_are_not_same(self):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = NEW_PARTIAL_DECK

        response_mock2 = Mock()
        response_mock2.status_code = 200
        response_mock2.json.return_value = NEW_PARTIAL_DECK
        response_mock2.json()['deck_id'] = "211111111111"
        # expected to be false
        self.assertEqual(response_mock.json()['deck_id'], response_mock2.json()['deck_id']) == False


if __name__ == '__main__':
    unittest.main()
