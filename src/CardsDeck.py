import requests
import webbrowser

# get a new unshuffled deck with
URL_NEW_DECK_UNSHUFFLED = 'https://deckofcardsapi.com/api/deck/new/'
URL_NEW_DECK_SHUFFLED = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
URL_DRAW_CARDS = 'https://deckofcardsapi.com/api/deck/<<deck_id>>/draw/?count='
class CardsDeck:

    @staticmethod
    def get_new_unshuffled_deck():
        api_result = requests.get(URL_NEW_DECK_UNSHUFFLED)
        api_response = api_result.json()
        print('Remaining cards: ' + str(api_response['remaining']) + ', '
              + 'Shuffled: ' + str(api_response['shuffled']) + ', '
              + 'DeckID: ' + str(api_response['deck_id']))
        return api_response

    @staticmethod
    def get_new_shuffled_deck():
        api_result = requests.get(URL_NEW_DECK_SHUFFLED)
        api_response = api_result.json()
        print('Remaining cards: ' + str(api_response['remaining']) + ', '
              + 'Shuffled: ' + str(api_response['shuffled']) + ', '
              + 'DeckID: ' + str(api_response['deck_id']))
        return api_response

    @staticmethod
    def draw_cards(deck_id=None):
        # deck_id will be used to draw cards from the same deck
        num = input('Enter number: ')
        # if deck_id exists->deck already created ->use the existing deck and deraw from it,\
        # otherwise create new deck and draw
        if deck_id:
            api_result = \
                requests.get('https://deckofcardsapi.com/api/deck/<<deck_id>>/draw/?count='
                             .replace('<<deck_id>>', deck_id) + str(num))
        else:
            api_result = requests.get('https://deckofcardsapi.com/api/deck/new/draw/?count=' + str(num))
        api_response = api_result.json()
        for i in range(0, len(api_response['cards'])):
            print(api_response['cards'][i]['code'] + ', '
                  + api_response['cards'][i]['suit'] + ', '
                  + api_response['cards'][i]['image'])
            webbrowser.open(api_response['cards'][i]['image'])
        return api_response

    @staticmethod
    def get_cards(select):
        if select == 1:
            CardsDeck.get_new_unshuffled_deck()

        if select == 2:
            CardsDeck.get_new_shuffled_deck()

        if select == 3:
            CardsDeck.draw_cards()
