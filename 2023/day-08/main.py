import numpy as np
import re

# ------------ PART 1 -------------
# Follow insane directions

filename = "data.txt"

f = open(filename, "r")
directions = f.readline().strip('\n')
data = [line.strip("\n").split() for line in f.readlines()][1:]
nodes = {}
for d in data:
    key = d[0]
    left = d[2][1:-1]
    right = d[3][:-1]
    nodes[key] = (left, right)

#print(directions)
#print(data)
#print(nodes)

def get_steps(directions, start, end):
    loc = start
    step_count = 0
    while loc != end:
        for d in directions:
            if d == "L":
                loc = nodes[loc][0]
            elif d == "R":
                loc = nodes[loc][1]
            else:
                break
            step_count += 1
    return step_count

steps = get_steps(directions, start="AAA", end="ZZZ")
print(f"Part 1 solution with {filename}: {steps} steps to reach ZZZ")

# Part 1 solution with data.txt: 16579 steps to reach ZZZ

# -------- PART 2 --------
# Now start positions are any that end in A
# End positions are any that end in Z
# Simultaneously move from all valid starts to any end
# Step count is equal to that which ensures you all arrive at the same time
# Lowest common multiple of individual paths
# If one path takes 2 steps to get to a valid end
# And another path takes 3 steps then total steps is
# Lowest common multiple of 2 and 3 = 6

def get_steps_to_end_z(directions, start):
    loc = start
    step_count = 0
    while loc[-1] != "Z":
        for d in directions:
            if d == "L":
                loc = nodes[loc][0]
            elif d == "R":
                loc = nodes[loc][1]
            else:
                break
            step_count += 1
    return step_count

start_positions = []
for key in nodes:
    if key[-1] == "A":
        start_positions.append(key)

all_steps = []
for sp in start_positions:
    steps = get_steps_to_end_z(directions, start=sp)
    all_steps.append(steps)


print(f"\nPart 2 solution with {filename}:\nStep count from each starting position to any **Z: {all_steps}\n" +
      f"Total steps is lowest common mutiple: {np.lcm.reduce(all_steps)}")

# Part 2 solution with data.txt:
# Step count from each starting position to any **Z: [14893, 19951, 22199, 16579, 17141, 12083]
# Total steps is lowest common mutiple: 12927600769609
# Data start positions: ['KTA', 'PLA', 'LJA', 'AAA', 'JXA', 'NFA']