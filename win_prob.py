from enum import IntEnum
from collections import Counter
from itertools import permutations
from itertools import combinations
import math
global BOARD_SIZE, DECK_SIZE, CARDS_PER_SUIT, NUM_SUITS
BOARD_SIZE = 5
DECK_SIZE = 52
CARDS_PER_SUIT = 13
NUM_SUITS = 4
NUM_EACH_RANK = 4




class Hands(IntEnum):
	ROYAL_FLUSH = 10
	STRAIGHT_FLUSH = 9
	FOUR_OF_A_KIND = 8
	FULL_HOUSE = 7
	FLUSH = 6
	STRAIGHT = 5
	THREE_OF_A_KIND = 4
	TWO_PAIR = 3
	PAIR = 2
	HIGH_CARD = 1

class Rank(IntEnum):
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	SIX = 6
	SEVEN = 7
	EIGHT = 8
	NINE = 9
	TEN = 10
	JACK = 11
	QUEEN = 12
	KING = 13
	ACE = 14


# win_prob: List-of tuples, int -> float
# calculates the win probability of a given poker hand
def win_prob(cards, num_players):
	pass


# has_x_of_a_kind: List-of tuples, int -> (bool, cards_remaining)
# finds whether or not there's a x-of a kind
def has_x_of_a_kind(cards, x):
	remaining = cards.copy()
	counts = Counter(i[0] for i in cards)
	for item in counts.items():
		if item[1] >= x:
			return True
	return False

# has_x_pair: List-of tuples, int -> bool
# finds whether or not it has x number of pairs
def has_x_pair(cards, x):
	counts = Counter(i[0] for i in cards)
	#filters out the number of pairs in the card list and checks whether it's >= the number of pairs we're looking for.
	return len(list(filter(lambda num: num >= 2, list(counts.values())))) >= x

pair_cards = [(Rank.SEVEN, 'H'), (Rank.SEVEN, 'D'), (Rank.TWO, 'H')]
print(has_x_pair(pair_cards, 2))

def has_pair(cards):
	return has_x_pair(cards, 1)

def has_two_pair(cards):
	return has_x_pair(cards, 2)

def has_trips(cards):
	return has_x_of_a_kind(cards, 3)

def has_quads(cards):
	return has_x_of_a_kind(cards, 4)

def has_full_house(cards):
	return has_trips(cards) and has_two_pair(cards)


# has_flush: List-of tuples, int -> bool
# checks if the cards have x amount of cards
# with the same suit
def has_flush(cards, x=5):
	suits = Counter([i[1] for i in cards])
	for i in suits.values():
		if i >= x:
			return True
	return False

def has_royal_flush(cards):
	possibilities = [
	[(Rank.TEN, 'D'), (Rank.JACK, 'D'), (Rank.QUEEN, 'D'), (Rank.KING, 'D'), (Rank.ACE, 'D')],
	[(Rank.TEN, 'S'), (Rank.JACK, 'S'), (Rank.QUEEN, 'S'), (Rank.KING, 'S'), (Rank.ACE, 'S')],
	[(Rank.TEN, 'C'), (Rank.JACK, 'C'), (Rank.QUEEN, 'C'), (Rank.KING, 'C'), (Rank.ACE, 'C')],
	[(Rank.TEN, 'H'), (Rank.JACK, 'H'), (Rank.QUEEN, 'H'), (Rank.KING, 'H'), (Rank.ACE, 'H')]
	]
	#total card value of a royal flush is 60:
	#10 + 11 + 12 + 13 + 14
	return has_straight_flush(cards) and any(all(item in cards for item in possibilities[i]) for i in range(len(possibilities)))

# has_x_straight: List-of tuples, int -> bool
# Returns whether or not it has a straight with
# x number of cards (standard is 5)
def has_straight(cards, x=5):
	for card in cards:
		ranks = [i[0] for i in cards]
		if straight_helper(ranks, card[0], x):
			return True
	return False


def has_straight_flush(cards):
	return has_straight(cards) and has_flush(cards)

# TODO: include support for A -> 5 straight

# straight_helper: List-of ints, int, int -> bool
# recursive function to check if there's a straight
# ranks: card ranks (e.g ['Ranks.SEVEN', 'Ranks.ACE'])
def straight_helper(ranks, next_card, cards_left):
	# base case
	if cards_left <= 0:
		return True
	# otherwise checks if the next card in order is 
	# in the cards
	if next_card in ranks:
		ranks.remove(next_card)
		return straight_helper(ranks, next_card + 1, cards_left - 1)
	return False

def has_high_card(cards):
	return True


# hand_prob: List-of tuples, HAND_TYPE -> float
# calculates the probability of getting the
# given hand with the current cards and board
# ex. hand_prob(cards, Hands.STRAIGHT)
def hand_prob(cards, potential_hand):
	# check if we already have that hand
	if hands_to_has_func[potential_hand](cards):
		return 1.0

	# otherwise return the probability we land that hand 

		pass
	#either they already have the hand or
	#they could get the hand based on the 
	#number of cards yet to be placed on the board
	pass

# each group of hand rankings
hand_ranking_groups = [
[Hands.FLUSH, Hands.STRAIGHT_FLUSH, Hands.ROYAL_FLUSH],
[Hands.STRAIGHT, Hands.STRAIGHT_FLUSH, Hands.ROYAL_FLUSH],
[Hands.PAIR, Hands.TWO_PAIR, Hands.FULL_HOUSE],
[Hands.PAIR, Hands.THREE_OF_A_KIND, Hands.FOUR_OF_A_KIND],
[Hands.HIGH_CARD]
]

# lose_prob: List-of Tuple, Hand, int -> float
# gets the probability of another player
# having a better hand 
def lose_prob(cards, hand, num_players):
	# All hands that >= this hand
	# If that hand_type == this hand_type then we check
	# the high cards to see which hand is better
	better_hands = list(filter(lambda x: x >= hand[0], Hands))
	print(better_hands)
	# accumulates with the probabilities of each
	# better base hand
	prob = 0.0
	for curr_hand in better_hands:
		pass
	for curr_group in hand_ranking_groups.copy():
		# the lowest hand in this grouping that beats the given hand
		base_hand = next(filter(lambda x: x >= hand[0], curr_group))
		prob += hands_to_prob_func[base_hand](cards)


# pair_prob: List-of Tuple -> float
# default total_cards is 7 (2 hole cards + 5 community cards)
# can be used with our cards or to calculate another players probability
# finds the probability of there being at least one pair once all cards
# are dealt
# ASSUMES all cards have unique ranks (there are no pairs currently)
def pair_prob(cards, total_cards=7):
	# the number of cards that have been dealt to us
	# and that are on the board
	# since we don't already have a pair, we can
	# assume each card has a unique rank
	num_cards = len(cards) # x
	# the number of cards remaining to be
	# dealt on the board
	cards_left = total_cards - num_cards # r
	# the number of different ways to arrange
	# the potential cards on the board
	perms = math.factorial(cards_left)

	# the number of cards left in the deck
	# after the paired card has been dealt
	brick_cards = DECK_SIZE - 1 - num_cards

	# the number of cards left in the deck
	# e.g 52 - 4 -> 48 cards left
	cards_in_deck = DECK_SIZE - num_cards
	# generally this would be equal to something like: 3 * (3C1 * 46C3 / 49C4)
	return num_cards * (math.comb(NUM_EACH_RANK - 1, 1) * math.comb(brick_cards, cards_left - 1) / math.comb(DECK_SIZE - num_cards, cards_left))




# rest_of_deck(name subject to change): 
def rest_of_deck(n, r, cards_left):
	if cards_left <= 0:
		return 1.0
	return math.combinations(n, r) * rest_of_deck(n - 1, r - 1, cards_left - 1)

# compares the 2 hands,
# a value > 0 indicates the first hand
# is greater
# a value < 0 indicates the second hand
# is greater
# a value = 0 indicatse the hands
# are equal.
def compare_hands(first, second):
	pass
	if first[0] != second[0]:
		return first[0] - second[0]
	return first[1] - second[1]
# A Hand can be represented as simply a Tuple containing the 
# Type of Hand and the highest card, e.g a Queen High Flush
# Can be represented as (FLUSH, Rank.QUEEN)
# Generally, a Hand is represented as (HAND_TYPE, HAND_RANK)
example_hand = (Hands.FLUSH, Rank.QUEEN)
example_worse_hand = (Hands.TWO_PAIR, Rank.ACE)
example_cards = [(Rank.QUEEN, 'D'), (Rank.ACE, 'D')]
example_board = [(Rank.QUEEN, 'C'), (Rank.KING, 'D'), (Rank.JACK, 'D'), (Rank.TWO, 'D')]
cards = example_board + example_cards


DECK = []
SUITS = ['D', 'C', 'H', 'S']
for rank in Rank:
	for suit in SUITS:
		DECK.append((rank, suit))


hands_to_has_func = {
	Hands.HIGH_CARD : has_high_card,
	Hands.PAIR : has_pair,
	Hands.TWO_PAIR : has_two_pair,
	Hands.THREE_OF_A_KIND : has_trips,
	Hands.STRAIGHT : has_straight,
	Hands.FLUSH : has_flush,
	Hands.FULL_HOUSE : has_full_house,
	Hands.FOUR_OF_A_KIND : has_quads,
	Hands.STRAIGHT_FLUSH : has_straight_flush,
	Hands.ROYAL_FLUSH : has_royal_flush
}

# a dictionary mapping each hand to the function
# which finds the probability of getting said hand
# given the players cards + the cards on the board
hands_to_prob_func = {
	
}

hands_to_has_func[1](cards)


#best_hand: List-of Tuple -> ()
def best_hand(cards):
	pass


no_pair_cards = [(Rank.SEVEN, 'H'), (Rank.EIGHT, 'D'), (Rank.SIX, 'H'), (Rank.NINE, 'D')]
print(has_straight(no_pair_cards))


print(3 * (math.comb(3, 1) * math.comb(48, 3) / math.comb(49, 4)))
print(math.comb(13, 5) / math.comb(50, 5))






