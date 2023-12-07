import re
import pandas as pd
import numpy as np
from itertools import islice

# ------------- PART 1 -------------
# Need to submit the lowest location value
# Start with the location destination range containing the lowest values
# Go backwards work out what range of Seeds fall into this
# Process these seeds only
# All data mappings start at 0, update test set to mirror

filename = "test3.txt"

# Get mappings as dict
d = {}
with open(filename, "r") as f:
    for group in f.read().split('\n\n'):
        key, *val = group.split(':\n')
        d[key] = sorted([[int(w) for w in v.split()] for v in val[0].split("\n")], key=lambda x: x[1])

# Pop (get & remove) seeds from dict
seeds = d.pop("seeds")[0]
# print(f"Seeds:\n{seeds}")
# print(f"Dict of mappings:\n{d}")

# I need the lowest location number that corresponds to a seed
# This must fall in one of the humidity-to-location ranges
# Start with the smallest location range [0, max] and trace path back
def reverse_path_trim(dictionary=d):
    return

# # Print the ranges
# for key in d:
#     print(f"\n{key}")
#     for r in d[key]:
#         print(f"D:[{r[0]},{r[0]+r[2]}] S:[{r[1]},{r[1]+r[2]}]")

def split_range(range1, subrange):
    """
    Input:
        range1: [start, end], end not include or included?
        range2: destination range
    Output: 
    
    """
    return
# Need a function that takes 2 mappings of ranges and convert them
# to one-one ranges of mappings. May start with a mapping containing
# only one range but this may split into many, each will need mapping
# Assume all ranges have min value 0 (true of data, but not of test.txt)
# test2.txt and test3.txt have the zeroes.

def shortcut(map1, map2, source_index, dest_index):
    """
    A function to work out the one-one map from a map to another map; 
    For example inputting the seed-soil map and the soil-fertilizer map
    outputs the seed-fertilizer map 
    Input:
        map1: list of lists of ranges described 
        [dest/source start, dest/source start, range] 
        map2: same format as map1
        source_index: index of source start value
        dest_index: index of destination start value
    Output:
        shortcut: one-one mapping direct from input of map1 to 
        output of map2
    """
    si = source_index
    di = dest_index

    # Sort map1 by destination and map2 by source
    map1 = sorted(map1, key=lambda x: x[di])
    map2 = sorted(map2, key=lambda x: x[si])

    # d[key] = sorted([[int(w) for w in v.split()] for v in val[0].split("\n")], key=lambda x: x[1])
    print(f"\n{map1}\n{map2}\n")

    map1_dest_mins = [v[di] for v in map1] + [map1[-1][di] + map1[-1][2]]
    map2_source_mins = [v[si] for v in map2] + [map2[-1][si] + map2[-1][2]]

    print(map1_dest_mins)
    print(map2_source_mins, "\n")

    munge = list(set(map1_dest_mins + map2_source_mins))
    print(munge)
    # munge_range = [i for i in munge[1:]]
    # munge_range = [[i,v] for i, v in enumerate(munge[1:])]
    munge_range = [[munge[i-1],munge[i]] for i in munge if i>0]

    print(munge_range)


    map1_source = [[m[si],m[si]+m[2]-1] for m in map1]
    map1_dest = [[m[di],m[di]+m[2]-1] for m in map1]
    map2_source = [[m[si],m[si]+m[2]-1] for m in map2]
    map2_dest = [[m[di],m[di]+m[2]-1] for m in map2]

    print(f"\n{map1_source}\n{map1_dest}\n{map2_source}\n{map2_dest}")

    # try
    outmap1 = []
    outmap2 = []
    for d in map1_dest:
        # find map2_source that map1_dest overlaps
        min_i = next(x for x, val in enumerate(map2_source) if d[0] <= val[1])
        max_i = next(x for x, val in enumerate(map2_source) if d[1] <= val[1])
        # overlap = [map2_source[i] for i in np.arange(min_i, max_i + 1)]
        # print(overlap)

        outmap1.append([map2_source[min_i][0],])
        for i in np.arange(min_i, max_i + 1):
            overlap = map2_source[i]
            print(overlap)




    print(outmap1, outmap2)
    return (outmap1, outmap2)

# Try backwards
# map1=d["humidity-to-location map"]
# map2=d["temperature-to-humidity map"]

# simpler test3 map; try backward: fertilzer to seed (via soil)
map1=d["soil-to-fertilizer map"] # fertilizer to soil
map2=d["seed-to-soil map"] # soil to seed

source_index = 0
dest_index = 1
output_map = shortcut(map1, map2, source_index, dest_index)
print(output_map)







##### ARCHIVE


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
# locations = []
# for s in seeds:
#     #print(f"Start seed: {s}")
#     mappings = [s]
#     for key in d:
#         s = find_map(start=s, sorted_map=d[key])
#     locations.append(s)

# # Submit the lowest location
# lowest_location = min(np.array(locations))
# print(f"Part 1 answer: {lowest_location}")

# Part 1 test answer: 35
# Part 1 data answer: 51580674