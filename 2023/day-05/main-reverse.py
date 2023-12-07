import numpy as np
import timeit
# -------- PART 2 --------
# Start with the smallest location value and check the output seed 
# exists in one of the given seed ranges
# irritatingly the map names do not aligin with the order of the columns


filename = "data.txt"

# Get reverse mappings as dict
# reverse them by sorting by 
d = {}
with open(filename, "r") as f:
    for group in f.read().split('\n\n'):
        key, *val = group.split(':\n')
        # Sort by first col "destination" when going forwards through the map
        # but "source" when reversing: x[0]
        d[key] = sorted([[int(w) for w in v.split()] for v in val[0].split("\n")], key=lambda x: x[0])

# Pop (get & remove) seeds from dict
seeds = d.pop("seeds")[0]
# print(seeds)
# print(d)

# refactor and reverse dictionary
rkeys = list(reversed(list(d.keys())))
# print(rkeys)
d2 = {}
for rkey in rkeys:
    source_start = [k[0] for k in d[rkey]]
    destination_start = [k[1] for k in d[rkey]]
    source_end = [k[0] + k[2] - 1 for k in d[rkey]]
    d2[rkey] = [source_start, destination_start, source_end]

# print(d2)

# Get list of locations to reverse map to seeds and check if the seed is valid
# The locations are in numerical order
location_start = d2['humidity-to-location map'][0]
location_end = d2['humidity-to-location map'][2]

locations = []
for ls, le in zip(location_start, location_end):
    locations.append(np.arange(start=ls, stop=le))
locations = np.concatenate(locations).ravel()
# print(locations)

# Get ranges of seeds to check in
seed_ranges = [[ss, ss + sr] for ss, sr in zip(seeds[0::2], seeds[1::2])]
# print(seed_ranges)

def find_map_2(start, source_start, destination_start, source_end):
    """
    Assumes all mappings include 0 (true for data.txt, but not test.txt)
    """
    if start > source_end[-1]:
        return start
    else:
        i = next(x for x, val in enumerate(source_end) if start <= val)
        output = start - source_start[i] + destination_start[i]
        return output



# Go through the locations list in order, starting with samllest (0)
# stop when find a valid seed

def get_lowest_valid_location():    
    for loc in locations:
        i = loc
        for key in d2:
            i = find_map_2(
                start=i,
                source_start=d2[key][0],
                destination_start=d2[key][1],
                source_end=d2[key][2]
            )
        for ss, sr in zip(seeds[0::2], seeds[1::2]):
            if ss <= i < (ss + sr):
                print(f"Location {loc} -> seed: {i}, in seed range [{ss}, {ss+sr-1}]")
                return (loc, i)


tic = timeit.default_timer()
res = get_lowest_valid_location()
toc = timeit.default_timer()

print(res)
print(f"Time taken: {toc - tic} seconds")
# print(f"Estimate time to process 100 million: {(toc-tic)/40*100000000/60} minutes")
# Estimate time to process 100 million: 18.325374791553866 minutes
# print(f"\n{valid_locs}\n{seeds_out}")
# print(f"\n{len(valid_locs)}\n{len(seeds_out)}")

# Location 99751240 -> seed: 1055427336, in seed range [1018893962, 1429853751]
# (99751240, 1055427336)
# Time taken: 1211.0272327959974 = ~20 mins










