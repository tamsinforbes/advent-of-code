import numpy as np
import re
import timeit

filename = "test.txt"

f = open(filename, "r")
data = [[list(r) for r in g.split("\n")] for g in f.read().split("\n\n")]
arrs = [np.array(d) for d in data]

# print(data)
print(arrs)

for a in arrs:
    print(a.shape)
# All dimensions of the mirror arrays are odd!

# ------- PART 1 -------
# Find the vertical or horizontal lines of reflection alternating over the mirrors
# Each mirror only reflects according to the rules in horix or vert axis
# Each row/col must exactly match its mirror, unless its mirror falls outside the 
# array
# Compare row 0 to end row and work up to h - work out where to stop based on where I am
# Code for horizontal reflection and transpose arr to get vertical
# For each mirror array count the number of columns to the left 
# of the vertical line of reflection and the number of rows above
# the horizontal line of refelction
# sum = cols_to_left + (100 * rows_above)

def count_horizontal_reflections(arr):
    """
    Input:
        arr: single mirror array to find horizontal reflection in
    Output:
        count: number of rows above horizontal reflection
    """
    matches_above = []
    for r in range(len(arr)):
        for s in range(r+1, len(arr)):
            if np.array_equal(arr[r], arr[s]):
                matches_above.append(r)
                print(f"Row {r} matches row {s}")
            else:
                print(f"Row {r} does not match row {s}")
    # Return number of rows above refelction line
    count = max(matches_above) + 1
    return count


def get_mirror_sum(arr):
    # get horizontal refelction count
    horiz_count = count_horizontal_reflections(arr)
    # get vertical reflection count
    vert_count = count_horizontal_reflections(np.transpose(arr))
    # sum according to the rule
    total = vert_count + 100 * horiz_count
    return total, horiz_count, vert_count

test = get_mirror_sum(arrs[0])
print(test)

# Argh misunderstood question
