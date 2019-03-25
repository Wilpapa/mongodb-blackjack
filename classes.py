import random
import pymongo

def last_eleven(hand,pos):
    """finds the first 11 in a list of number

    :param hand: A list, of numbers
    :param pos: An int, position to start searching from
    :rtype: An int, position where 11 was found, or 99 if not found
    """
    i=pos
    found=99
    while i<=(len(hand)-1):
        if hand[i]==11:
            found=i
            i=99
        i+=1
    return(found)

def is_blackjack(hand):
    """returns true if the list contains [1,10] or [10,1]"""
    if (hand[0]==1 and hand[1]==10) or (hand[1]==1 and hand[0]==10):
        return(True)
    else:
        return(False)

class Deck:
    """Represents a full set of 52 cards desks to play with

    :param nb_decks: An int, number of card decks to use
    """
    def __init__(self,nb_decks):
        self.nb_decks=nb_decks
        self.mid_deck = 26*nb_decks #used to re-shuffle deck and reset position
        self.shuffle_deck()
        
    def shuffle_deck(self):
        """Creates a deck of nb_decks 52 cards games and shuffles it"""
        self.position_deck = 0
        self.cards=list(range(1,11))*4*self.nb_decks+[10,10,10]*self.nb_decks*4
        random.shuffle(self.cards)
        
    def get_card(self):
        """Retrieves the card at position_deck position and increases position_deck
        if half the cards have been played, reshuffle and rest position_deck"""
        card = self.cards[self.position_deck]
        self.position_deck+=1
        if (self.position_deck>self.mid_deck):
            self.shuffle_deck()
        return(card)

class Player:
    """Represents a player drawing cards - human or casino"""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the player hand for each new game"""
        self.hand=[]
        self.blackjack=False
        self.score=0
        self.gain=-1

    def draw_card(self,deck):
        """Draw a card from the deck and calculate player hand score"""
        self.hand.append(deck.get_card())
        self.score_hand()

    def score_hand(self):
        """Calculate player's hand score

        Unless a blackjack is detected, scoring is made by counting all aces as 11,
        then switch them back to 1 one after the other until score goes below 22
        """
        if len(self.hand)==2:
            self.blackjack=is_blackjack(self.hand)
            hand=self.hand
        else:
            score=0
            pos=0
            # let's convert all 1 in 11
            hand = [11 if x==1 else x for x in self.hand]
            # compute score and switch back aces to 1 until score<=21
            while (sum(hand)>21 and pos<99):
            # if over 21 then change last 11 for 1
                pos=last_eleven(hand,pos)
                if pos<99:
                    hand[pos]=1
        self.score=sum(hand)

    def add_gain(self, value):
        self.gain+=value

class DAO:
    """Represents MongoDB blackjack.games collection to write each game into

    :param uri: A string, MongoDB URI to connect to
    """
    def __init__(self,uri):
        # connect to mongo
        connection = pymongo.MongoClient(uri)

        # get a handle to the MongoDB database
        self.db = connection.blackjack
        self.games = self.db.games
        
    def add_game(self,start_time,sample,threshold,p_human,p_casino):
        game =  { "TS" : start_time,
                    "sample" : sample,
                    "threshold" : threshold,
                    "playerHand" : p_human.hand,
                    "casinoHand" : p_casino.hand,
                    "playerBlackjack" : p_human.blackjack,
                    "casinoBlackjack" : p_casino.blackjack,
                    "playerScore" : p_human.score,
                    "casinoScore" : p_casino.score,
                    "playerGain" : p_human.gain }
                
        self.games.insert_one(game)
