import numpy as np
import re
import timeit

filename = "data.txt"

# get data into array first (don't put this inside a loop please)
arr = np.genfromtxt(
    fname=filename,
    dtype=str,
    delimiter=1,
    filling_values='f',
    deletechars=None,
    comments=None # auto set to #
)

# print(arr)

# transpose array, get string of every row (col)
# for each row split at the fixed rocks (#) roll the round rocks (O)
# left (north) and join back with #

def tilt_west(arr):
    """
    Input: arr: to be be tilted west; manipulate array first to tilt
                north, south, east.
    Output; tilted_array
    """
    tilted = []
    for r in arr:
        # split each row string at #
        parts = "".join(r).split("#")
        # for each subset sort the 0 to the LHS (West)
        sorted_parts = [sorted(p, reverse=True) for p in parts]
        # previous splits each part into list of elements, so rejoin them
        rejoin_parts = [''.join(s) for s in sorted_parts]
        # join each part with # into a string
        rejoin_string = "#".join(rejoin_parts)
        # now split it into individual elements to go back into array
        tilted.append(list(rejoin_string))
    
    return np.array(tilted)

# Now count the value of the load
# count the number of Os in each row and multiple by nrows - row index

def north_beam_load(arr):
    load = 0
    n_rows = arr.shape[0]
    for r in range(n_rows):
        matches = re.findall("O", "".join(arr[r]))
        load += len(matches) * (n_rows - r)
    return load


def spin_cycle(arr):
    """
    Input: arr: array
    Output: spun: array tilted North, West, South then East
    """
    # Tilt North
    tilted = np.transpose(tilt_west(np.transpose(arr)))
    # print(f"Tilted North\n{tilted}")
    # Tilt West
    tilted = tilt_west(tilted)
    # print(f"Tilted North then West\n{tilted}")
    # Tilt South (rotate anticlockwise 3 times to bring S to W, then once more)
    tilted = np.rot90(tilt_west(np.rot90(tilted, 3)), 1)
    # print(f"Tilted North, West then South\n{tilted}")
    # Tilt East (first flip left rght to bring E to W then back)
    tilted = np.fliplr(tilt_west(np.fliplr(tilted)))
    return tilted


# get the first match
def get_indices_of_sequence(spins):
    for s1 in range(len(spins)):
        for s2 in range(s1 + 1, len(spins) - s1):
            if np.array_equal(spins[s1], spins[s2]):
                # print(f"Spin {s1 + 1} matches spin {s2}")
                return (s1, s2)


# Given a the sequence of loads/spin outputs
# Work out which spin/load coincides with the nth value in the sequence
def get_nth_load(n, seq_indices, loads_sample):
    """
    Input:
        n: the nth load value to return
        seq_indices: (m, n) tuple of indices where the spin outputs match
        m is the start index of the pattern and n the index it repeats at
        hence the pattern is in [m, n), includes m but not n
        loads_sample: the sample list of loads from the beginning and including
        one cycle of the sequence
    Output:
        nth_load: the load value that coincides with the nth position
        in the sequence
    """
    # length of sequence before repeats
    non_repeater_length = seq_indices[0]
    repeater_length = seq_indices[1] - seq_indices[0]
    repeater = loads_sample[seq_indices[0]:seq_indices[1]]

    # find position in repeating pattern at nth position 
    seq = (n - non_repeater_length) % repeater_length - 1 # appear to be one over so take one off
    load = repeater[seq]
    return load, seq, repeater, non_repeater_length, repeater_length


# ----------- PART 1 -------------
# Transpose array so that tilt_west actually tilts north then transpose back
tilted_north = np.transpose(tilt_west(np.transpose(arr)))
part_1_load = north_beam_load(tilted_north)
print(f"Part 1 with {filename}: total North beam load when tilted North: {part_1_load}")
# Part 1 with data.txt: total load when tilted North: 108889

# ----------- PART 2 --------------
# Spin cycle tilts north, west, south, east in that order
# run spin cycle 1000,000,000 times (except don't)
# There must be some repeating cycle; find the cycle; work out what part
# of the cycle it is on at the trillionth spin - that is the answer
# continue spinning until current spin equals first spin; this is the repeat point
# Doesn't matter if Part 1 north tilt is included or not since the first
# spin starts by tilting north and two tilts in the same direction have the same effect

a = np.array([[".","O","#"],["O",".","."],["#",".","."],[".","O","O"]])
# It takes some spins for the pattern to settle down
# So continue whle loop until a spin config matches a previous spin config
start = arr
n_iters = 289 # 289 is the smallest number of iterations to get the repeating pattern
# pattern repeats index (138, 152), but something wrong with how I'm searching
# It should find it after around 160 spins, but needs more twice as many
# as the end of the sequence
# run 2 spins
first_spin = spin_cycle(start)
first_spin_load = north_beam_load(first_spin)
t = spin_cycle(first_spin)
second_spin_load = north_beam_load(t)
count = 1
# Get a sample of the  spin output and hope this contains the repeating pattern
spins = [first_spin, t]
loads = [first_spin_load, second_spin_load]
print(f"Spin 0 configuration has load: {loads[0]}")
print(f"Spin 1 configuration has load: {loads[1]}")
for n in range(n_iters):
    count += 1
    t = spin_cycle(t)
    load = north_beam_load(t)
    spins.append(t)
    loads.append(load)
    #print(f"Spin {count} configuration has load: {load}")

# print(spins[0:4])
# print(loads)

print(f"\nGet bounds of the repeating pattern in the sequence:")
seq_indices = get_indices_of_sequence(spins)
print(f"Pattern start: {seq_indices}")

n = 1000000000
output = get_nth_load(n, seq_indices, loads)
print(f"Part 2 with {filename}: {n}th load value: {output[0]}")

# Part 2 with data.txt: 1000000000th load value: 104671
# This gives 65, instead of 64 - I wonder if the Part 1 Northward tilt should be included
# no it doesn't matter - I may just be 1 out
# Yep I was one out - can't count clearly
