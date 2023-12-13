import exrex
import numpy as np
# from itertools import combinations, combinations_with_replacement, permutations
import re
import timeit
# import math
import multiprocessing as mp


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


# Refactor possible_ways() to receive only 1 argument for ease of passing to mp pool
def possible_ways(record):
    """
    Input:
        record: list of two items: ["uuuuguugbbb", [1,2,3]], first represents unknown,
        good and bad springs and second is a list of numbers of adjecent bad springs
    Output:
        w: number of possible configurations of bad/good springs
    """
    # Get possible configs from record 1
    exrex_pattern = make_exrex(record[0])
    configs = list(exrex.generate(exrex_pattern))

    # Get pattern from record 2
    pattern = make_pattern(record[1])
    num_springs = len(record[0])

    all_matches = []
    for c in configs:
        matches = re.findall(pattern, c)
        # print(c, matches)
        for m in matches:
            # print(f"length: {len(m)}")
            if len(m) == num_springs:
                all_matches.append(m)

    return len(all_matches)  


# ----------- PART 2 ------------
# Now the number get rather larger; time current method to assess feasibilty
# Each record1  is repeated 5 times with an extra ? (u) in between
# Each record 2 is repeated 5 times (with a comma separator)

# record1 = "????.######..#####." # len=12
# record2 = [1,6,5]
# # these currently have 10 possibilities, and apparntly have 506250 arrangements after
# # expanding
# exp_record1 = ((record1.replace("?", "u").replace(".","g").replace("#","b") + "u") * 5)[:-1] # drop final u
# exp_record2 = record2 * 5

# Expand the data
exp_data = []
for d in data2:
    exp_rec1 = ((d[0].replace("?", "u").replace(".","g").replace("#","b") + "u") * 5)[:-1] # drop final u
    exp_rec2 = d[1] * 5
    exp_data.append([exp_rec1, exp_rec2])

# print(f"Expanded data:\n{exp_data}")

# ----------------------------------#
######### MULTIPROCESSING ###########
#-----------------------------------#



tic = timeit.default_timer()

# chunk data
num_of_chunks = 10
n = round(len(exp_data) / num_of_chunks)
print(f"Number of chunks: {n}")
print(f"Number of CPUS: {mp.cpu_count()}")
# create chunks
chunks = [exp_data[i:i + n] for i in range(0, len(exp_data), n)]

total_ways = [] # list of total ways from each chunk
chunk_index = 0
for chunk in chunks:
    def main():
        pool = mp.Pool(mp.cpu_count())
        ways = pool.map(possible_ways, chunk)
        total_ways.append(ways)
        print(f"Number of arrangements for {len(chunk)} records in chunk: {ways}")

    if __name__ == "__main__":
         main()
    print(f"Running total number of arrangements: {total_ways}")

toc = timeit.default_timer()

# Part 2 multiplying by 5 results in at least n^5 more ways (I think)
print(f"Part 2 time taken to process {filename} with {len(data2)} rows: {toc - tic} seconds")
print(f"Part 2 with {filename}: Total arrangements for each chunk: {total_ways}")
print(f"Part 2 with {filename}: Total arrangements {sum(total_ways)}")
