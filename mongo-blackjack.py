"""Simulates blackjack games

Simulates blackjack games with a single player agains the casino
with a defined threshold for player to stop drawing

Writes the games into a MongoDB collection named "blackjack.games"
for later analysis

Before starting, set up the following constants :
SAMPLES = 1000  # number of games to play
THRESHOLD = 15  # score under which Player will draw 1 card
NB_DECKS = 4  # number of decks to use. Decks are reshuffled when half the cards have been drawn
"""

from datetime import datetime
from classes import DAO, Player, Deck

MONGO_URI = "mongodb://localhost"  
SAMPLES = 10000 
THRESHOLD = 15 
NB_DECKS = 4  
START_TIME = datetime.now()

print("starting Blackjack games simulator at", START_TIME)
print(" SAMPLES",SAMPLES)
print(" THRESHOLD",THRESHOLD)
print(" NB_DECKS",NB_DECKS)
mongo = DAO(MONGO_URI)
p_human = Player()
p_casino = Player()
c_deck = Deck(NB_DECKS)

print("Deck generated in",datetime.now()-START_TIME,"seconds")
for i in range(SAMPLES):
    p_human.draw_card(c_deck)
    p_casino.draw_card(c_deck)
    p_human.draw_card(c_deck)
    p_casino.draw_card(c_deck)

    if p_human.blackjack:
        if p_casino.blackjack:
            p_human.gain = 0  # Casino and Player both have a blackjack, it's a deuce
        else:
            p_human.gain = 2  # Player alone has a Blackjack, double win
    else:
        while p_human.score < THRESHOLD:  # Player will draw cards until reaching THRESHOLD score
            p_human.draw_card(c_deck)
        if p_human.score <= 21:
            while p_casino.score < 17:  # by Casino rules, Casino will draw cards until scoring 17 or more
                p_casino.draw_card(c_deck)
            if p_casino.score > 21:
                p_human.gain = 1  # Casino lost
            elif p_human.score > p_casino.score:
                p_human.gain = 1  # Player has a better hand than the Casino
            elif p_human.score == p_casino.score:  # both have 21 but Player has no blackjack
                if not p_casino.blackjack:
                    p_human.gain = 0  # deuce only if Casino has no blackjack either

    mongo.add_game(START_TIME, i, THRESHOLD, p_human, p_casino)
    p_human.reset()
    p_casino.reset()
print("done in",datetime.now()-START_TIME,"seconds")
print(datetime.now())