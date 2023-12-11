import re
import pandas as pd
import numpy as np

# ---------------- PART 1 ---------------

# Similar to Dy 3 except sliding "window" is a "cross"
# No diagonal movement (yet)
# Find S to start, for each discovered section of pipe
# Check where to go next
# S is connected to exactly 2 sections of pipe (we ignore how
# the animal actually got into this apparently closed loop)
# Return the step number counting from 0 of the half way position
# That is the furtherst point from Start; the highest step count
# before getting nearer to start again

filename = "test6.txt"

# get data into array first (don't put this inside a loop please)
data = np.genfromtxt(
    fname=filename,
    dtype=str,
    delimiter=1,
    filling_values='f',
    deletechars=None,
    comments=None # auto set to #
)
print(data)

# Find S start position
start = np.where(data == "S")
#print(start, start[0], start[1])


# Adapted from Day 3
def cross_positions(array_shape=(1,1), start=(0,0), previous=None):
    """
    Input:
        start_position: the start position of the centre of the cross
        array_shape: (num_row, num_col) of the given array
        previous: previous position
    Output:
        labelled: list of labelled arrays of valid frame positions (label, position)
    """
    # Arrays are arranged (y,x) (row:y, col:x) going 
    cross_mask = np.array([(-1,0), (0,-1), (1,0), (0,1)]) # N W S E
    # Add start position to mask
    positions = np.array(start) + cross_mask
    # Add position label
    labels = ["N", "W", "S", "E"]
    # Drop invalid positions (outside array or previous position)
    labelled = []
    for label, p in zip(labels, positions):
        if (0 <= p[0] < array_shape[0]) and (0 <= p[1] < array_shape[1]) and ((p[0],p[1]) != previous):
            # print((p[0],p[1]), previous)
            labelled.append((label, (p[0], p[1])))
   
    return labelled


def pipe_from_start(arr, start_marker="S"):
    """
    Return the first found (of the two possible) 2 valid pipes connected to 
    the start position.
    """
    valid_pipe_map = {
        "N":["7","|","F"],
        "S":["J","|","L"],
        "W":["L","-","F"],
        "E":["7","-","J"]
    }
    # Find start position
    start = np.where(arr == start_marker)
    # Get labelled positions valid for array
    positions = cross_positions(array_shape=arr.shape, start=(start[0][0], start[1][0]))
    # Return first valid map
    for p in positions:
        pipe = arr[p[1]]
        if pipe in valid_pipe_map[p[0]]:
            return (pipe, p[1]), (start_marker, (start[0][0],start[1][0]))


def find_next_pipe(arr, current, previous):
    """
    Find the next pipe section to move to from a point inside the loop
    (not the start). Do not check previous position.
    Input: 
        arr: array of pipes
        current: current value and position in array (value, (row, col)) in array (absolute)
        previous: None or previous value and position in array (value, (row, col)) in array (absolute)
    """

    valid_pipe_map = {
        "N": (["7","|","F"], "S"),
        "S": (["J","|","L"], "N"),
        "W": (["L","-","F"], "E"),
        "E": (["7","-","J"], "W")
    }
    # get valid positions to check (excludes previous position and positions external to array)
    positions = cross_positions(arr.shape, current[1], previous[1])
    # Find the first valid pipe (should be only one possible)
    current_pipe = arr[current[1]]
    for p in positions:
        next_pipe = arr[p[1]]
        to_dir = p[0]
        from_dir = valid_pipe_map[to_dir][1]
        if next_pipe in valid_pipe_map[to_dir][0] and current_pipe in valid_pipe_map[from_dir][0]:
            return (next_pipe, p[1]), current
        # elif next_pipe == "S":
        #     return (next_pipe, p[1]), current

        # print(next_pipe, current_pipe)
        # if (current_pipe in valid_pipe_map[p[0]]) and (next_pipe in valid_pipe_map[p[1]]):
        #     return (next_pipe, p[1]), current


# ------- Run --------
# Find start position and get first found (of 2 possible) next pipe from start
current, previous = pipe_from_start(data, start_marker='S')
print(current, previous)
# Loop over the remaining pipes inthe loop until reach start again
step_count = 1
while current[0] != "S":
    step_count += 1
    print(f"{current}, {previous}")
    current, previous = find_next_pipe(data, current, previous)

print(step_count)
print(f"Part 1 solution with {filename}:\nTotal step count: {step_count}, furthest point in loop: {step_count/2}")

# Part 1 solution with test1.txt:
# Total step count: 8, furthest point in loop: 4.0
# With data.txt counted 13630 total steps, and furthest position: 6815 CORRECT
# Don't fully understand why, nor why my while loop doesnt't break nicely - my function didn't deal with "S" when it got back there

# I have not considered how to establish I'm back at the start in a loop that grazes the Start ie test6.txt
# mess....
# Got lucky to get the correct answer for part 1; my code that doen not deal with "S" near the end does
# count the correct steps just doesn't break nicely; errors when it can't compare "S" in the if statement linem 107
# Anyway moving on with my life...
