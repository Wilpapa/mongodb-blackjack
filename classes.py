import random
import pymongo

class Deck:
    """Represents a full set of 52 cards desks to play with

    :param nb_decks: An int, number of card decks to use
    """
    def __init__(self, nb_decks):
        self.nb_decks = nb_decks
        self.mid_deck = 26 * nb_decks  # used to re-shuffle deck and reset position
        self.shuffle_deck()

    def shuffle_deck(self):
        """Creates a deck of nb_decks 52 cards games and shuffles it"""
        self.position_deck = 0
        self.cards = 4 * self.nb_decks * (list(range(1, 11)) + [10, 10, 10])
        random.shuffle(self.cards)

    def get_card(self):
        """Retrieves the card at position_deck position and increases position_deck
        if half the cards have been played, reshuffle and rest position_deck"""
        card = self.cards[self.position_deck]
        self.position_deck += 1
        if self.position_deck > self.mid_deck:
            self.shuffle_deck()
        return card

class Player:
    """Represents a player drawing cards - human or casino"""
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the player hand for each new game"""
        self.hand = []
        self.blackjack = False
        self.score = 0
        self.gain = -1

    def draw_card(self, deck):
        """Draws a card from the deck and calculate player's hand score"""
        self.hand.append(deck.get_card())
        self.score_hand()

    def score_hand(self):
        """Calculates player's hand score

        Unless a blackjack is detected, scoring is made by counting all aces as 11,
        then switch them back to 1 one after the other until score goes below 22
        """
        self.blackjack = (self.hand==[1,10] or self.hand==[10,1])
        if self.blackjack:
            self.score = 21
        else:
            # convert all aces to 11
            hand = [11 if x == 1 else x for x in self.hand]
            # compute score and switch back aces to 1 until score<=21
            while sum(hand) > 21:
                try:
                    i = hand.index(11) # any 11 in hand ?
                    hand[i] = 1 # yes switch it to 1
                except ValueError: # no, let's exit
                    break
            self.score = sum(hand)

class DAO:
    """Represents MongoDB blackjack.games collection to write each game into

    :param uri: A string, MongoDB URI to connect to
    """
    def __init__(self, uri):
        connection = pymongo.MongoClient(uri)
        self.db = connection.blackjack
        self.games = self.db.games

    def add_game(self, start_time, sample, threshold, p_human, p_casino):
        """writes game result to blackjack.games database"""
        game = {"TS": start_time,
                "sample": sample,
                "threshold": threshold,
                "playerHand": p_human.hand,
                "casinoHand": p_casino.hand,
                "playerBlackjack": p_human.blackjack,
                "casinoBlackjack": p_casino.blackjack,
                "playerScore": p_human.score,
                "casinoScore": p_casino.score,
                "playerGain": p_human.gain}
        self.games.insert_one(game)
