import numpy as np
from itertools import combinations


# ---------------- PART 1 ---------------
# Shortest path between galaxies post expansion

filename = "data.txt"

# get data into array
raw = np.genfromtxt(
    fname=filename,
    dtype=str,
    delimiter=1,
    filling_values='f',
    deletechars=None,
    comments=None # auto set to #
)

# print(raw)
# convert to 0s and number galaxies
data = np.zeros(raw.shape, dtype=int)
g = 1
for r in range(data.shape[0]):
    for c in range(data.shape[1]):
        if raw[r,c] == "#":
            data[r,c] = g
            g += 1

# print(data)

# Get empty rows
empty_rows = []
for r in range(data.shape[0]):
    if np.all(data[r]==0):
        empty_rows.append(r)

# Get empty cols
empty_cols = []
data_t = np.transpose(data)
for r in range(data_t.shape[0]):
    if np.all(data_t[r]==0):
        empty_cols.append(r)

# Insert extra rows
expanded = data.copy()
extra_row_adjust = 0
for r in empty_rows:
    expanded = np.insert(
        expanded, r + extra_row_adjust, (0), axis=0
    )
    extra_row_adjust += 1

# Insert extra cols
extra_col_adjust = 0
for c in empty_cols:

    expanded = np.insert(
        expanded, c + extra_col_adjust, (0), axis=1
    )
    extra_col_adjust += 1

# print(expanded.shape,"\n", expanded)

# get galaxy positions
g_pos = []
for r in range(expanded.shape[0]):
    for c in range(expanded.shape[1]):
        if expanded[r,c] > 0:
            g_pos.append((r,c))
# print(g_pos)
pairs = list(combinations(g_pos, 2))
# print(pairs, "\n", len(pairs))

# For each pair of galaxy positions the shortest path
# is described as the horiz and vert distance to it
distances = []
total = 0
for p in pairs:
    row_dist = abs(p[1][0] - p[0][0])
    col_dist = abs(p[1][1] - p[0][1])
    total += row_dist + col_dist
    distances.append((row_dist, col_dist))

# print(distances)

print(f"Part 1 with {filename}: Total distance between pairs of galaxies: {total}")



# ------ PART 2 -------
# Expansion is actually 1,000,000 times
# For every empty row/col insert 1,000,000 empty row/cols
# Get distances from original and then calculate new distances with expansion based on position

def get_data(filename):
    # read data
    raw = np.genfromtxt(
        fname=filename,
        dtype=str,
        delimiter=1,
        filling_values='f',
        deletechars=None,
        comments=None # auto set to #
    )
    # convert to 0s and number galaxies
    data = np.zeros(raw.shape, dtype=int)
    g = 1
    for r in range(data.shape[0]):
        for c in range(data.shape[1]):
            if raw[r,c] == "#":
                data[r,c] = g
                g += 1
    return data

# function to adjust for expansion
def adjust_distance(pair, empty_rows, empty_cols, factor=10):
    """
    Input:
        pair: pair of galaxy locations to adjust
        adjustment: factor to multiply empty rows/cols
        empty_rows: list of empty row numbers
        empty_cols: list of empty col numbers
    Output:
        adj_dist: Distance between the given pair adjusted for expansion
    """
    adjustment = factor - 1
    row_pair = sorted([pair[0][0], pair[1][0]])
    col_pair = sorted([pair[0][1], pair[1][1]])
    # print(f"Check pair order: {pair}, {row_pair}, {col_pair}")
  
    row_dist = abs(row_pair[1] - row_pair[0])
    col_dist = abs(col_pair[1] - col_pair[0])

    # Paits are pairwise in order but not colwise
    # Get number of empty rows between galaxies
    num_empty_rows = len([r for r in empty_rows if row_pair[0] < r < row_pair[1]])
    # Get number of empty cols between galaxies
    num_empty_cols = len([c for c in empty_cols if col_pair[0] < c < col_pair[1]]) 

    adj_row_dist = row_dist + num_empty_rows * adjustment
    adj_col_dist = col_dist + num_empty_cols * adjustment
    adj_dist = adj_row_dist + adj_col_dist
    return adj_dist

# -------- PART 2 RUN ------------
data = get_data(filename)
# print(data)

# Get empty rows
empty_rows = []
for r in range(data.shape[0]):
    if np.all(data[r]==0):
        empty_rows.append(r)

# Get empty cols
empty_cols = []
data_t = np.transpose(data)
for r in range(data_t.shape[0]):
    if np.all(data_t[r]==0):
        empty_cols.append(r)

# Get pairs of galaxy positions
g_pos = []
for r in range(data.shape[0]):
    for c in range(data.shape[1]):
        if data[r,c] > 0:
            g_pos.append((r,c))
pairs = list(combinations(g_pos, 2))

# print(f"Empty rows: {empty_rows}")
# print(f"Empty cols: {empty_cols}")
# print(pairs)

# test = adjust_distance(((0, 3), (4, 6)), empty_rows, empty_cols, adjustment=10)
# print(test)

adjusted_dists = []
for p in pairs:
    ad = adjust_distance(p, empty_rows, empty_cols, factor=1000000)
    adjusted_dists.append(ad)
# print(adjusted_dists)
print(f"Part 2 with {filename}: Adjusted total distance: {sum(adjusted_dists)}")

# Part 2 with data.txt: Adjusted total distance: 568914596391