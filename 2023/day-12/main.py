import exrex
import numpy as np
# from itertools import combinations, combinations_with_replacement, permutations
import re
import timeit
# import math


# ------------ PART 1 -------------------
filename = "test.txt"
f = open(filename, "r")
raw = [d.strip("\n").split(" ") for d in f.readlines()]
data = [[r[0], [int(i) for i in r[1].split(",")]] for r in raw]

# replace record 1 with letters rather than special characters
# ? -> U (unknown), . -> G (good), # -> B (bad)
data2 = []
for d in data:
    new = d[0].replace("?", "u").replace(".","g").replace("#","b")
    data2.append([new, d[1]])


# function to generate the expression for exrex
def make_exrex(record1):
    res = record1.replace("u", "[bg]")
    return res


# function to generate pattern for re
def make_pattern(record2):
    """
    Input:
        record2: list of numbers eg [1,1,3]
    Output:
        pattern: pattern string to feed to re.findall()
    """
    pattern = "g*"
    for n in record2:
        pattern += "b" * n + "g+"
    # swap final "+" for "*"
    pattern = pattern[:-1] + "*"
    return pattern


def possible_ways(record1, record2):
    """
    Input:
        record1: "uuuuguugbbb" unknown, good and bad springs
        record2: [1,2,3] sets of bad springs
    Output:
        w: number of possible configurations of bad/good springs
    """
    # Get possible configs from record 1
    exrex_pattern = make_exrex(record1)
    configs = list(exrex.generate(exrex_pattern))

    # Get pattern from record 2
    pattern = make_pattern(record2)
    num_springs = len(record1)

    all_matches = []
    for c in configs:
        matches = re.findall(pattern, c)
        # print(c, matches)
        for m in matches:
            # print(f"length: {len(m)}")
            if len(m) == num_springs:
                all_matches.append(m)

    return len(all_matches)  


total_ways = 0
for d in data2:
    ways = possible_ways(d[0], d[1])
    print(f"{d}: Number of ways: {ways}")
    total_ways += ways

print(f"\nPart 1 with {filename}: total ways for all rows of springs: {total_ways}")

# Part 1 with data.txt: total ways for all rows of springs: 7939


# ----------- PART 2 ------------
# Now the number get rather larger; time current method to assess feasibilty
# Each record1  is repeated 5 times with an extra ? (u) in between
# Each record 2 is repeated 5 times (with a comma separator)
record1 = "????.######..#####." # len=12
record2 = [1,6,5]
# these currently have 10 possibilities, and apparntly have 506250 arrangements after
# expanding
exp_record1 = ((record1.replace("?", "u").replace(".","g").replace("#","b") + "u") * 5)[:-1] # drop final u
exp_record2 = record2 * 5
print(exp_record1, exp_record2)

tic = timeit.default_timer()

# ways = possible_ways(exp_record1, exp_record2)

toc = timeit.default_timer()

print(f"Time taken to calculate {ways} arrangements: {toc - tic} seconds")
# Time taken to calculate 2500 arrangements: 74.50608092802577 seconds
# Time taken to calculate ~500000 arrangements: KILLED 😔