"""Simulates blackjack games

Simulates blackjack games with a single player agains the casino
with a defined threshold for player to stop drawing

Writes the games into a MongoDB collection named "blackjack.games"
for later analysis
"""

from datetime import datetime
from classes import *


MONGOURI="mongodb://localhost" #MongoDB connection string
SAMPLES=1000 #number of games to play
THRESHOLD=15 #score under which player will draw 1 card
NB_DECKS=4 #number of decks to use. Decks are reshuffled when half the cards have been drawn
START_TIME=datetime.now()

mongo=DAO(MONGOURI)
p_human=Player()
p_casino=Player()
c_deck=Deck(NB_DECKS)

for i in range(SAMPLES):
    p_human.draw_card(c_deck)
    p_casino.draw_card(c_deck)
    p_human.draw_card(c_deck)
    p_casino.draw_card(c_deck)
    
    if p_human.blackjack:
        if p_casino.blackjack:
            p_human.gain=0 # casino and player both have a blackjack, it's a deuce
        else:
            p_human.gain=2 # player has a blackjack, double win
    else:
        while (p_human.score<THRESHOLD): # player will draw cards until reaching THRESHOLD score
            p_human.draw_card(c_deck)
        if (p_human.score<=21):
            while (p_casino.score<17): # by casion rule, bank wil draw cards until scoring 17 or more
                p_casino.draw_card(c_deck)
            if (p_casino.score>21):
                p_human.gain=1 # casino loses
            elif (p_human.score>p_casino.score):
                p_human.gain=1 # player overscores casino
            elif (p_human.score==p_casino.score): # both have 21 but player has no blackjack
                if not p_casino.blackjack:
                    p_human.gain=0 # deuce only if Casino has no blackjack either
                    
    
    mongo.add_game(START_TIME, i, THRESHOLD, p_human, p_casino)
    p_human.reset()
    p_casino.reset()
