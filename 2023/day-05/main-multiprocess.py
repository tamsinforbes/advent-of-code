import re
import pandas as pd
import numpy as np
from itertools import islice
import time
import timeit
import multiprocessing as mp
import random

filename = "data.txt"
# NB: Altered input data to put the seed values on the next line so the layout is
# the same for each group, added map from 0 to test (test2.txt) as data.txt includes
# 0 in each map.

# Read mappings from file into
d = {}
with open(filename, "r") as f:
    for group in f.read().split('\n\n'):
        key, *val = group.split(':\n')
        d[key] = sorted([[int(w) for w in v.split()] for v in val[0].split("\n")], key=lambda x: x[1])

# Pop (get & remove) seeds from dict
seeds = d.pop("seeds")[0]

# function to get next map
def find_map(start, sorted_map):
    source_start = [k[1] for k in sorted_map]
    destination_start = [k[0] for k in sorted_map]
    source_end = [k[1] + k[2] - 1 for k in sorted_map]

    if (start < source_start[0]) or (start > source_end[-1]):
        return start
    else:
        i = next(x for x, val in enumerate(source_end) if start <= val)
        output = start - source_start[i] + destination_start[i]
        return output

# Find the lowest location value for any of the input seeds
tic = timeit.default_timer()
# print(seeds)
locations = []
for s in seeds:
    #print(f"Start seed: {s}")
    mappings = [s]
    for key in d:
        s = find_map(start=s, sorted_map=d[key])
    locations.append(s)

toc = timeit.default_timer()

# PART 1 ANSWER ---36769984
# Submit the lowest location
lowest_location = min(np.array(locations))
total_seeds = len(seeds)
dur = toc - tic
print(f"\nPart 1 lowest location using: {filename}: {lowest_location}")
print(f"Part 1 time taken to map {total_seeds} seeds: {dur} seconds")
print(f"Part 1 estimated time for 1.7 billion seeds: {dur / total_seeds * 1700000000 / 60 / 60} hours\n")

#####-----------------------------------------------------------#######
#------------------------ PART 2 Multiprocessnig ---------------------#
#####-----------------------------------------------------------#######

# Now the list of 20 seeds is actually a seed start value followed by a range
# Get seeds
seed_ranges = seeds[1::2]
seeds_start = seeds[0::2]
seeds = []
for s, r in zip(seeds_start, seed_ranges):
    seeds.append(np.arange(start=s, stop=s+r))
seeds = np.concatenate(seeds).ravel()

total_seeds = sum(seed_ranges)

# Refactor dictionary of mappings so that each mapping comprises
# a list of 3 lists: source_start, destination_start, source_end
# So this is only done ONCE!
d2 = {}
for key in d:
    source_start = [k[1] for k in d[key]]
    destination_start = [k[0] for k in d[key]]
    source_end = [k[1] + k[2] - 1 for k in d[key]]
    d2[key]=[source_start, destination_start, source_end]


# Refactor function to get next map
def find_map_2(start, source_start, destination_start, source_end):
    """
    Assumes all mappings include 0 (true for data.txt, but not test.txt)
    """
    if start > source_end[-1]: # if (start < source_start[0]) or (start > source_end[-1]):
        return start
    else:
        i = next(x for x, val in enumerate(source_end) if start <= val)
        output = start - source_start[i] + destination_start[i]
        return output


# Wrap into single input function so it is easy to pass to multiprocessing pool
def seed_to_location(s):
    #print(mp.current_process())
    for key in d2:
        s = find_map_2(
            start=s,
            source_start=d2[key][0],
            destination_start=d2[key][1],
            source_end=d2[key][2])
    return s





# # Multiprocessing
# tic = timeit.default_timer()
# def main():
#     pool = mp.Pool(mp.cpu_count())
#     locations = pool.map(seed_to_location, seeds)

#     print(f"Part 2 lowest location using: {filename}: {min(np.array(locations))}")

# if __name__ == "__main__":
#     main()

# toc = timeit.default_timer()
# print(f"Part 2 time taken to map {total_seeds} seeds: {toc - tic} seconds")
# print(f"Part 2 estimated time for 1.7 billion seeds: {(toc - tic) / total_seeds * 1700000000 / 60 / 60} hours")





# Multiprocessing
tic = timeit.default_timer()

# seeds chunks
n = 170000000
#n = 100000
chunks = [seeds[i:i + n] for i in range(0, len(seeds), n)]
#print(len(chunks))

chunk_lowest_locations = []
for chunk in chunks:
    def main():
        pool = mp.Pool(mp.cpu_count())
        locations = pool.map(seed_to_location, chunk)
        chunk_lowest_locations.append(min(np.array(locations)))

    if __name__ == "__main__":
         main()
    print(chunk_lowest_locations)
print(chunk_lowest_locations)
print(min(np.array(chunk_lowest_locations)))
print(f"Part 2 lowest location using: {filename}: {min(np.array(chunk_lowest_locations))}")


toc = timeit.default_timer()
print(f"Part 2 time taken to map {total_seeds} seeds: {toc - tic} seconds")
#print(f"Part 2 estimated time for 1.7 billion seeds: {(toc - tic) / total_seeds * 1700000000 / 60 / 60} hours")

# Part 2 answer using data.txt: 99,751,240
# In chunk index 4, found after about 30 mins
# So in the middle of the range

# [189555255, 726585356, 828243961, 239722699, 99751240, 2314484766, 270062277, 1139784462, 868993622, 105230362]
# 99751240
# Part 2 lowest location using: data.txt: 99751240
# Part 2 time taken to map 1680883088 seeds: 4809.141869252999 seconds: 1.3 hours
