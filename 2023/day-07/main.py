import numpy as np
import pandas as pd
import re
from pandas.core.base import PandasObject

# set file
filename = "test.txt"

# get data into df
df = pd.read_table(filename, delimiter=" ", header=None, names=["hand", "bid"])
hands = list(df["hand"])
bids = list(df["bid"])
data = []
for h, b in zip(hands, bids):
    data.append([h,b])

# Order hands by card order first
card_alphabet = "AKQJT98765432"
card_order = dict(zip(card_alphabet, range(len(card_alphabet))))
# sort lists of lists by 0th element in each sublist (hand[0]) 
sorted_data = sorted(data, key=lambda hand: [card_order[c] for c in hand[0]])
# put back into df
df = pd.DataFrame(sorted_data, columns = ["hand", "bid"])

# ---------- PART 1 ----------
# Camel cards - similar to poker, but CARD ORDER MATTERS
# cards: A K Q J T 9 8 7 6 5 4 3 2 (Ace high, T=10)
# Rank by hand type and then card value
# order matters: so TAAAA and Q2222 are both type 4 of a kind
# but Q2222 is ranked higher because it's first card Q is higher than 
# T the first card of TAAAA

# Function to determine hand type
def hand_type(hand):
    # hand type order corresponds to set length
    hand_types = [["1-5K"], ["2-4K", "3-FH"], ["4-3K", "5-2P"], ["6-1P"], ["7-HC"]]
    s = len(set(hand))
    if s in [1,4,5]:
        return hand_types[s-1][0]
    elif s == 2: # test 1 card to distinguish 4K from FH
        # 1 or 4 matches indicates 4K
        if len(re.findall(hand[0], hand)) in [1,4]:
            return hand_types[s-1][0]
        # 2 or 3 matches indicates FH
        else:
            return hand_types[s-1][1]
    elif s == 3: # test 2 cards to distinguish 2P from 3K
        first_card_matches = len(re.findall(hand[0], hand))
        second_card_matches = len(re.findall(hand[1], hand))
        matches = set([first_card_matches, second_card_matches])
        # any 2 matches indicates 2P
        if 2 in matches:
            return hand_types[s-1][1]
        # otherwise 3K (matches 3 or 1 card)
        else:
            return hand_types[s-1][0]
    else:
        return None


# Add hand_type column to df
df["hand_type"] = df["hand"].apply(hand_type)

# sort by hand_type (df already ordered by hand)
# NB use kind='mergesot' in sort values to ensure any existing desired other 
# column order is retained. The default sort will randomly shuffle for efficiency
df.sort_values(by=["hand_type"], axis=0, inplace=True, kind='mergesort')

# WEAKEST HAND GETS rank = 1 (opposite of what I have done)
df["strongest_first_rank"] = df["hand_type"].rank(method="first")
df["weakest_first_rank"] = df["strongest_first_rank"].rank(ascending=False)
# Multiply bid by rank
df["score"] = df["bid"] * df["weakest_first_rank"]
# print(df)

print(f"Part 1 sum of scores using: {filename}: {sum(df['score'])}")

# Part 1 sum of scores using: data.txt: 250946742.0
# Part 1 sum of scores using: test.txt: 6440

# 250645833 too low !!! I have ranked this correctly I think
# 250354667 too low !!! I had ranked it strongest first
# 250946742.0 CORRECT: use kind='mergesot' in sort values to ensure any existing
# other order is retained. The default sort will randomly shuffle as this is more
# efficient


# ------------- PART 2 --------------
# J is now Joker, a wild card and the card_order has changed
# Any Js should become the cards required to make the best hand type
# What actual card they becaome id irrelevant as any hand type ties 
# are broken based on the ordering depending on original card value

# get data into df
df = pd.read_table(filename, delimiter=" ", header=None, names=["hand", "bid"])
hands = list(df["hand"])
bids = list(df["bid"])
data = []
for h, b in zip(hands, bids):
    data.append([h,b])

# Order hands by card order first
card_alphabet = "AKQT98765432J"
card_order = dict(zip(card_alphabet, range(len(card_alphabet))))
# sort lists of lists by 0th element in each sublist (hand[0]) 
sorted_data = sorted(data, key=lambda hand: [card_order[c] for c in hand[0]])
# put back into df
df = pd.DataFrame(sorted_data, columns = ["hand", "bid"])
#print(df)

hand_types = [["1-5K"], ["2-4K", "3-FH"], ["4-3K", "5-2P"], ["6-1P"], ["7-HC"]]
# Apply this function to the hand_types column with a mapping?
def joker_hand_type(hand, hand_type):
    """
    Input: 
        hand: Hand of 5 cards 
        hand_type: Hand type determined in part one
    Output: best_hand: best hand possible with other cards
    """
    # Number of jokers in hand
    j = len(re.findall("J",hand))
    # Set length of hand
    s = len(set(hand))

    if j in [0, 5]: # 0 or 5 Js -> hand_type is unchanged
        return hand_type
    elif s == 2: # 2 cards in set: [4K, FH] -> 4K
        return "1-5K"
    elif s == 3:
        if j in [2, 3]: # [3K, 2P] -> 4K
            return "2-4K"
        elif hand_type == "4-3K":
           return "2-4K"
        elif hand_type == "5-2P":
            return "3-FH"
    elif s == 4: # 4 cards in set: 1P -> 3K (always choose 3K over 2P)
        return "4-3K"
    elif s == 5: # 5 cards in set: HC -> 1P
        return "6-1P"
    else:
        return None


# Add hand_type column to df
df["hand_type"] = df["hand"].apply(hand_type)

# Add joker_hand_type column to df
df["joker_hand_type"] = df.apply(
    lambda x: joker_hand_type(x["hand"], x["hand_type"]),
    axis=1
)


# sort by hand_type (df already ordered by hand)
# NB use kind='mergesot' in sort values to ensure any existing desired other 
# column order is retained. The default sort will randomly shuffle for efficiency
df.sort_values(by=["joker_hand_type"], axis=0, inplace=True, kind='mergesort')

# WEAKEST HAND GETS rank = 1 (opposite of what I have done)
df["strongest_first_rank"] = df["joker_hand_type"].rank(method="first")
df["weakest_first_rank"] = df["strongest_first_rank"].rank(ascending=False)
# Multiply bid by rank
df["score"] = df["bid"] * df["weakest_first_rank"]
print(df)

print(f"Part 2 sum of scores using: {filename}: {sum(df['score'])}")

# Part 2 sum of scores using: test.txt: 5905.0
# Part 2 sum of scores using: data.txt: 251824095.0