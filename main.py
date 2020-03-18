from time import sleep
from CardLogic import CardsDeck

#def clear():
#    sleep(3)
#    os.system('clear')


def close():
#    clear()
    print("program has been closed")
    sleep(1)
    exit(0)


def main():
    while True:
        print("""
        1. Get a brand new deck
        2. Get a brand new *shuffled* deck
        3. Enter number of cards to draw
        4. Draw a cheating 4 aces deck
        5. Exit
        """)

        menu = input()
    #    clear()  # clear the screen
        switcher = {
            1: lambda x: CardsDeck.get_cards(1),
            2: lambda x: CardsDeck.get_cards(2),
            3: lambda x: CardsDeck.get_cards(3),
            4: lambda x: CardsDeck.get_cards(4),
            5: lambda x: close(),
        }
        switcher.get(int(menu))(0)


if __name__ == "__main__":
    main()
