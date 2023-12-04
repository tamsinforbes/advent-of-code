import numpy as np
# ------------ PART 1 -----------
# Scratch cards; each card has a set of winning numbers (first set)
# and a set of chosen numbers (second set)
# Find the set intersection; the chosen numbers that appear in the
# winning numbers set. 
# The score for the card is 2^(m-1) for m matching numbers
# 1 point for 1 number, 2 for 2, 4 for 3, 8 for 4
# and 0 for no matches
# Find the score of each card and submit the sum of all the scores


filename = "test.txt"
f = open(filename, "r")
cards = [line.strip("\n") for line in f.readlines()]

#print(cards)
total = 0
card_number = 0
card_matches = []
for c in cards:
    card_number += 1
    numbers = c.split(": ")[1].split(" | ")
    winners = set(map(int, numbers[0].split()))
    chosen = set(map(int, numbers[1].split()))
    matches = chosen.intersection(winners)
    if len(matches) > 0:
        score = 2**(len(matches)-1)
    else:
        score = 0
    card_matches.append(len(matches))
    total += score

print("Part 1 total score:", total)
#print(card_matches)

# PART 1 answer: 21485

# --------------- PART 2 --------------
# Count total number of cards after processing:
# A card with n matches creates copies the next n cards
# (so copies can only be of card numbers greater than the spawning card number)
# The number of matches dictates how many subsequent cards are copied
# The current count of the card in question dictates how many copies of each subsequent card to make

index = np.arange(1, len(cards)+1)
#print(f"Index: {index}")
#print(f"Card matches: {card_matches}")
card_count = np.array([1] * len(index)) # start with 1 instance of each card
#print(f"Sart card count: {card_count}")
#print(card_count.shape)

for i, cm in zip(index, card_matches):
    # number of cards
    nc = len(index)
    # for each card update the card count
    # next cm cards are incremented by the current card count value
    # current card count
    cc = card_count[i-1]
    #print(f"current card count: {cc}")
    count_update = np.array(i*[0] + cm*[cc] + (nc-cm-i)*[0])
    #print(f"Current count update to apply: {count_update}")
    # apply count_update
    card_count = card_count + count_update
    print(f"Current card count: {card_count}")



#print(f"Final card count: {card_count}")
print(f"Total card count Part 2: {sum(card_count)}")

# Part 2 test answer: 30
# Part 2 data answer: 11024379