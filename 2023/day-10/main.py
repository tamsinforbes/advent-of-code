import re
import pandas as pd
import numpy as np

# ---------------- PART 1 ---------------
# What is the furthest step count from the start along the loop

filename = "data.txt"

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



# Given current and previous find next
def next_pipe(arr, current_loc=(0,0), came_from="N"):
    """
    Input:
        arr:
        current_loc: tuple current location eg: (0,0)
        came_from: direction came from, one of N, S, W, E.
    Output:
        next_loc: next location as tuple eg (1,1)
        next_came_from: direction came from; one of N, S, W, E 
    """
    pipe_to_dir = {
        "F": ["S", "E"],
        "7": ["S", "W"],
        "L": ["N", "E"],
        "J": ["N", "W"],
        "|": ["N", "S"],
        "-": ["W", "E"]
    }

    # Convert direction travelling to to direction came from 
    # from the perspective of next move
    to_from = {"N": "S", "S": "N", "W": "E", "E":"W"}
    # Map direction to change in positions
    dir_to_mask = {"N": (-1,0), "S": (1,0), "W": (0,-1), "E": (0,1)}

    current_pipe = arr[current_loc]
    move = [d for d in pipe_to_dir[current_pipe] if d != came_from][0]
    # Get next position
    next_loc = (current_loc[0] + dir_to_mask[move][0], current_loc[1]+dir_to_mask[move][1])
    # Get next came_from
    next_came_from = to_from[move]
    return next_loc, next_came_from

def get_next_from_start(arr, start_marker="S"):
    """
    Input:
        arr: array
        start_marker: character that indicates the starting position
    Output:
        start: start location eg (0,0)
        next_loc: location of next pipe from start
        came_from: direction from Start to get there, one of N, S, W, E.
    """
    valid_pipe_map = {
        "N":["7","|","F"],
        "S":["J","|","L"],
        "W":["L","-","F"],
        "E":["7","-","J"]
    }
    # Find start position
    start = np.transpose(np.where(arr == start_marker))
    # Arrays are arranged (y,x) (row:y, col:x) going 
    cross_mask = np.array([(-1,0), (0,-1), (1,0), (0,1)]) # N W S E
    # Add start position to mask
    positions = start + cross_mask
    # Add position label
    labels = ["N", "W", "S", "E"]
    # Convert direction travelling to to direction came from 
    # from the perspective of next move
    to_from = {"N": "S", "S": "N", "W": "E", "E":"W"}
    # Drop invalid positions (outside array)
    positions_lab = []
    for label, p in zip(labels, positions):
        if (0 <= p[0] < arr.shape[0]) and (0 <= p[1] < arr.shape[1]):
            positions_lab.append((label, (p[0], p[1])))
    # Return first valid map
    for p in positions_lab:
        pipe = arr[p[1]]
        if pipe in valid_pipe_map[p[0]]:
            next_loc = p[1]
            came_from =to_from[p[0]]
            return (start[0][0], start[0][1]), next_loc, came_from

def get_s_pipe(arr, start=(0,0)):
    """
    Get the type of pipe hidden under the "S" start position
    Input:
        arr: array
        start: position of start of pipe
    Output:
        start_pipe: character representing type of pipe under
            start marker.
    """
    valid_pipe_map = {
        "N":["7","|","F"],
        "S":["J","|","L"],
        "W":["L","-","F"],
        "E":["7","-","J"]
    }
    dir_to_pipe = {
        "SE": "F", "SW": "7", "NE": "L", "NW": "J", "NS": "|", "WE": "-",
        "ES": "F", "WS": "7", "EN": "L", "WN": "J", "SN": "|", "EW": "-",
    }

    # Get positions around start
    cross_mask = np.array([(-1,0), (0,-1), (1,0), (0,1)]) # N W S E
    # Add start position to mask
    positions = start + cross_mask
    # Add position label
    labels = ["N", "W", "S", "E"]

    # Label and drop positions outside array
    positions_lab = []
    for label, p in zip(labels, positions):
        row = p[0]
        col = p[1]
        n_rows = arr.shape[0]
        n_cols = arr.shape[1]
        pipe = arr[row, col]
        if (0 <= row < n_rows) and (0 <= col < n_cols):
            positions_lab.append((label, (row, col), pipe))
    
    # Drop invalid pipes
    valid_positions = []
    for p in positions_lab:
        pipe = arr[p[1]]
        if pipe in valid_pipe_map[p[0]]:
            valid_positions.append(p)
    
    # Check exactly two valid_positions
    # Again get pipe type
    if len(valid_positions) == 2:
        dirs = "".join([valid_positions[0][0], valid_positions[1][0]])
        start_pipe = dir_to_pipe[dirs]
    else:
        print(f"Number of valid pipes next to start not exactly equal to 2!")

    return start_pipe





# ---------- PART 1 RUN -----------
start, current_loc, came_from = get_next_from_start(data, "S")
print(f"Start values: S location: {start}\nNext pipe location: {current_loc}; Came from: {came_from}")

step = 1
while current_loc != start:
    step += 1
    current_loc, came_from = next_pipe(data, current_loc, came_from)

print(f"Part 1 with {filename}: Total steps: {step}; Furthest number of steps from start: {step/2}")
# Start values: S location: (62, 61)
# Next pipe location: (62, 60); Came from: E
# Part 1 with data.txt: Total steps: 13630; Furthest number of steps from start: 6815.0



# ---------------------------------------
# ---------------- PART 2 ---------------
# How many tiles are enclosed by the loop?
# Completely enclosed, like an enclave (ground or other pipe, just not loop)

# Get all positions of tiles in the loop
loop_positions = []
start, current_loc, came_from = get_next_from_start(data, "S")
loop_positions.append(start)

while current_loc != start:
    loop_positions.append(current_loc)
    current_loc, came_from = next_pipe(data, current_loc, came_from)

# Get start pipe type and all the other loop pipes
start, current_loc, came_from = get_next_from_start(data, "S")
start_pipe = get_s_pipe(data, start)
loop_pipes = [start_pipe]
for pos in loop_positions[1:]:
    loop_pipes.append(data[pos])

for pos, pipe in zip(loop_positions, loop_pipes):
    print(pos, pipe)

# Create new array of just the loop and not the loop
loop = np.zeros(data.shape, dtype=object)
for pos, pipe in zip(loop_positions, loop_pipes):
    loop[pos] = pipe
# Swap zeros for dots
loop[loop==0] = "."
print(f"loop dimnesions: {loop.shape}\n{loop}")

# Loop properties
# Reading from the left 
# Of the 6 pipes: F L J 7 | -
# F L are vert to horiz:
# J 7 are horiz to vert
# | vert to veet
# - horiz to horiz
# F, L, are always first in a row containing horizontal wall
# - is always in the middle of other horizontal pipes
# J 7 are always last in a section of horizontal wall: they NEVER start (from the left)
# | is always in the middle of other vertical pipes

# Scan horizontally
inner_count = 0
for r in loop:
    # # Keep track of horizonal wall
    # wall = 0
    # Keep track of in/outsde loop
    state = 0
    # Keep track of previous corner pipe
    last_corner = "X"
    print(f"Running count: {inner_count}")
    for c in r:
        if c == "|":
            if state == 0:
                state = 1
                print(f"{c} inside")
            elif state == 1:
                state = 0
                print(f"{c} outside")
        elif c in ["F", "L"]:
            if state == 0:
                state = 1
                last_corner = c
                print(f"{c} inside")
            elif state == 1:
                state = 0
                last_corner = c
                print(f"{c} outside")
        elif c == "7":
            if last_corner == "F":
                if state == 0:
                    state = 1
                    print(f"{c} inside")
                elif state == 1:
                    state = 0
                print(f"{c} outside")
            elif last_corner == "L":
                print(f"{c} No state change")
        elif c == "J":
            if last_corner == "L":
                if state == 0:
                    state = 1
                    print(f"{c} inside")
                elif state == 1:    
                    state = 0
                    print(f"{c} outside")
            elif last_corner == "F":
                print(f"{c} No state change")
        elif state == 1 and c == ".":
            inner_count += 1
            print(f"{c} Internal dot!!!")
        elif state == 0 and c == ".":
            print(f"{c} external dot")
        elif c == "-":
            print(f"{c} Stuck in the wall :o(")
        else:
            print(f"Uncaptured condition")

print(f"Part 2 with {filename}: Total count of internal dots: {inner_count}")
            
# Part 2 with data.txt: Total count of internal dots: 269
