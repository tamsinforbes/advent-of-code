import re
import pandas as pd
import numpy as np
from itertools import islice


filename = "test.txt"
# NB: Altered input data to put the seed values on the next line so the layout is
# the same for each group
# No gaps in the ranges, just before or after

# Get mappings as dict
d = {}
with open(filename, "r") as f:
    for group in f.read().split('\n\n'):
        key, *val = group.split(':\n')
        d[key] = sorted([[int(w) for w in v.split()] for v in val[0].split("\n")], key=lambda x: x[1])

# Pop (get & remove) seeds from dict
seeds = d.pop("seeds")[0]
print(f"Seeds:\n{seeds}")
print(f"Dict of mappings:\n{d}")

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

# Now what was the actual question?
# print(seeds)
locations = []
for s in seeds:
    #print(f"Start seed: {s}")
    mappings = [s]
    for key in d:
        s = find_map(start=s, sorted_map=d[key])
    locations.append(s)

# Submit the lowest location
lowest_location = min(np.array(locations))
print(f"Part 1 answer: {lowest_location}")

# Part 1 test answer: 35
# Part 1 data answer: 51580674


# ------------ PART 2 -------------
# Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac,
# it looks like the seeds: line actually describes ranges of seed numbers.

# The values on the initial seeds: line come in pairs. Within each pair, the first value is the
# start of the range and the second value is the length of the range. So, in the first line of the example above:

# seeds: 79 14 55 13

seed_ranges = seeds[1::2]
seeds_start = seeds[0::2]
#print(seeds_start, seed_ranges)

seeds = []
for s, r in zip(seeds_start, seed_ranges):
    seeds.append(np.arange(start=s, stop=s+r))
seeds = np.concatenate(seeds).ravel()

# Now what was the actual question?
# print(seeds)
locations = []
for s in seeds:
    #print(f"Start seed: {s}")
    mappings = [s]
    for key in d:
        s = find_map(start=s, sorted_map=d[key])
    locations.append(s)

# Find all the locations and submit the lowest location
lowest_location = min(np.array(locations))
print(f"Part 2 answer: {lowest_location}")

# Part 2 test answer: 46
# Part 2 data answer: re-read the question!!!!