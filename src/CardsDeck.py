import requests
import webbrowser

class CardsDeck:

    @staticmethod
    def getNewCardDeck():
        api_result = requests.get('https://deckofcardsapi.com/api/deck/new/')
        api_response = api_result.json()
        print('Remaining cards: ' + str(api_response['remaining']) + ', '
              + 'Shuffled: ' + str(api_response['shuffled']) + ', '
              + 'DeckID: ' + str(api_response['deck_id']))
        return api_response

    @staticmethod
    def getShuffledDeck():
        api_result = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
        api_response = api_result.json()
        print('Remaining cards: ' + str(api_response['remaining']) + ', '
              + 'Shuffled: ' + str(api_response['shuffled']) + ', '
              + 'DeckID: ' + str(api_response['deck_id']))
        return api_response

    @staticmethod
    def drawCards():
        num = input('Enter number: ')
        api_result = requests.get('https://deckofcardsapi.com/api/deck/new/draw/?count=' + str(num))
        api_response = api_result.json()
        for i in range(0, len(api_response['cards'])):
            print(api_response['cards'][i]['code'] + ', '
                  + api_response['cards'][i]['suit'] + ', '
                  + api_response['cards'][i]['image'])
            webbrowser.open(api_response['cards'][i]['image'])
        return api_response

    @staticmethod
    def getCards(type):
        if(type == 1):
            CardsDeck.getNewCardDeck()

        if(type == 2):
            CardsDeck.getShuffledDeck()

        if(type == 3):
            CardsDeck.drawCards()
