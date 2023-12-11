import re
import pandas as pd
import numpy as np

# ---------------- PART 1 ---------------
# What is the furthest step count from the start along the loop

filename = "test7.txt"

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



# ---------- RUN -----------
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

# ---------------- PART 2 ---------------
# How many tiles are enclosed by the loop?
# Completely enclosed, like an enclave (ground or other pipe, just not loop)

# Get all the parts of the loop
loop_tiles = []
start, current_loc, came_from = get_next_from_start(data, "S")
loop_tiles.append(start)

while current_loc != start:
    loop_tiles.append(current_loc)
    current_loc, came_from = next_pipe(data, current_loc, came_from)

# Create new array of just the loop and not the loop
raster = np.zeros(data.shape)
for tile in loop_tiles:
    raster[tile] = 1
print(f"Raster dimnesions: {raster.shape}\n{raster}")

# Create new array of just the pipe tiles
pipe_arr = np.chararray(data.shape)
for tile in loop_tiles:
    pipe_arr[tile] = data[tile]
print(f"\n{pipe_arr}")



# Raster scan an update wether in or out of the loop
# for r in raster:
#     for c in r:
#         print(c)

state = 0
inner_count = 0
tiles_scanned = 0
for r in raster:
    # count 1s in row
    ones_in_row = sum(r)
    print(f"Ones in row: {ones_in_row}")
    # state = 0
    # for c in r:
    #     tiles_scanned += 1
    #     c_int = np.round(c)
    #     print(c)
    #     print(c == 0)
    #     print(state == 0)
    #     print(np.round(c) == 1)

    #     if state == 0 and c_int == 1:
    #         state = 1
    #         print("inside")
    #     elif state == 1 and c_int == 0:
    #         inner_count += 1
    #     elif state == 1 and c_int == 1:
    #         state = 0
    #     elif state == 0 and c_int == 0:
    #         continue

total_tiles = raster.shape[0] * raster.shape[1]
print(f"End state: {state}; Inner tile count: {inner_count}")
print(f"All {total_tiles} tiles scanned: {tiles_scanned == total_tiles} ({tiles_scanned} tiles scanned).")
# state = 0, c = 0
# state = 0, c = 1
# state = 1, c = 0
# state = 1, c = 1

# Scan each row with a sliding window of 2 tiles
# rows = raster.shape[0]
# cols = raster.shape[1]

# state = 0
# wall = 0
# total_count = 0
# tiles_scanned = 0
# for r in range(rows):
#     state = 0
#     for c in range(cols-1):
#         row_count = 0
#         tiles_scanned += 1
#         win = [int(raster[r,c]), int(raster[r, c+1])]
#         # print(f"Tile: {r, c} window: {win} state: {state} inner count: {inner_count}")
#         if state == 0 and win == [1,0]:
#             state = 1
#         elif state  == 1 and win == [0,0]:
#             row_count += 1 
#         elif state == 1 and win == [0,1]:

#         elif state == 1 and win == [0,1]:
#             state = 0
#         print(f"Tile: {r, c} window: {win} state: {state} inner count: {row_count}")
#     total_count += row_count


# total_tiles = raster.shape[0] * raster.shape[1]
# print(f"End state: {state}; Total count: {total_count}")
# print(f"Scanning sliding window of two tiles.")
# print(f"All {total_tiles} tiles scanned: {tiles_scanned + cols == total_tiles}")
