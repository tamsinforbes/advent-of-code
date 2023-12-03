import re
import pandas as pd
import numpy as np

# ------------- PART 1 ---------------
# The engine schematic (your puzzle input) consists of a visual representation of the engine.
# There are lots of numbers and symbols you don't really understand, but apparently any number
# adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum.
# (Periods (.) do not count as a symbol.)

# Here is an example engine schematic:

# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..

# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol:
# 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a
# part number; their sum is 4361.

# Of course, the actual engine schematic is much larger. What is the sum of all of the part
# numbers in the engine schematic?

# get data into array
# get start position and length of numbers, and number itself
# create a frame of positions to check around each number
# get position of all symbols and the position of all digits
# compare number positions to symbol positions in rows above, same and below

def frame_mask(length=1):
    """
    Input:
        length: length of window centre, assume centre on one row only
    Output:
        mask: array of row and col differnces to calculate frame positions 
    """
    # col to left of start position
    left = [(-1,-1), (0,-1), (1,-1)]
    # col to right of end posistion
    right = [(-1,length), (0,length), (1,length)]
    # middle cols of lag and lead rows
    middle = []
    for i in range(length):
        middle.append((-1,i))
        middle.append((1, i))

    mask = left + middle + right
    return np.array(mask)

def frame_positions(start_position=(0,0), length=1, array_shape=(1,1)):
    """
    Input:
        start_position: the start position of the centre of the window
        length: length of window centre, assume centre on one row only
        array_shape: (max_row, max_col) of the given array
    Output:
        positions_valid: array of valid frame positions 
    """
    # add start position to mask
    positions = np.array(start_position) + frame_mask(length)
    # tidy positions to drop values outside array dimensions
    positions_valid = np.delete(
        positions, np.where(
            (positions[:, 0] < 0) | (positions[:, 0] >= array_shape[0]) |
            (positions[:, 1] < 0) | (positions[:, 1] >= array_shape[1])
            )[0],
            axis=0
        )        
    return positions_valid

def check_frame(arr, positions, pattern=r"[^.0-9]"):
    """
    Input:
        arr: numpy array
        positions: array of valid positions within arr
        pattern: regex pattern to check in each position
    Output:
        Bool: True if pattern match found
    """
    # Get the characters around the window centre
    frame_chars = []
    for p in positions:
        frame_chars.append(arr[p[0],p[1]])
    # if any of the frame_chars match the pattern return true
    match = re.search(pattern, "".join(frame_chars))
    if match is not None:
        return True
    return False

def get_frame_matches(arr, posiitons, pattern=r"[0-9]"):
    """
    Input:
        arr: numpy array
        positions: array of valid positions within arr
        pattern: regex pattern to check in each position
    Output:
        frame_chars: the posiitons and values of the matches
    """
    # Get the values and positions of the matches
    frame_matches = []
    for p in positions:
        match = re.search(pattern, arr[p[0],p[1]])
        if match is not None:
            frame_matches.append([p, arr[p[0],p[1]]])
    return frame_matches

# Get the things given by the pattern, their start position and length
def get_things(filename, pattern=r"\d+"):
    """
    Input:
        filename: text file to read in
        pattern: regex pattern to match on
    Output:
        things: list of lists of match value, (row, col) start position, and length
    """
    # read file
    f = open(filename, "r")
    data = [line.strip("\n") for line in f.readlines()]
    # for each line in the file
    things = []
    row_count = 0
    for d in data:
        matches = re.finditer(pattern, d)
        for match in matches:
            things.append([
                (match.group()),
                (row_count, match.span()[0]),
                match.span()[1]-match.span()[0],
            ])
        row_count += 1
    return things

# PART 1 test answer: 4361
# PART 1 final answer: 520019

# ------------------ PART 2 ----------------
# Each asterix adjacent to exactly 2 numbers is a gear
# Its gear ratio is the prodcut of those 2 numbers
# Sum these products

# Find all the asterixes
# Get window frame positions around each asterix
# chek these for numbers 
# check against my list of numbers



#### TESTING ###
filename = "data.txt"

# get data into array first (don't put this inside a loop please)
darray = np.genfromtxt(
    fname=filename,
    dtype=str,
    delimiter=1,
    filling_values='f',
    deletechars=None,
    comments=None # auto set to #
)
#print(darray)

numbers = get_things(filename, pattern=r"\d+")
# print(f"Numbers: total matches: {len(numbers)}; {numbers}")
asterixes = get_things(filename, pattern=r"[*]")
# print(f"Asterixes: total matches: {len(asterixes)}; {asterixes}")


# Assume only stand alone asterixes per row ie * on the same row
# and no **, *** etc on the same row
# All asterixes hence have length 1, so all use the same window frame mask
frame_length_one = frame_mask(length=1)

# apply to each asterix position then for each of these positions
# check if it coincides with a number position


total = 0
for n in numbers:
    positions = frame_positions(
        start_position=n[1], length=n[2], array_shape=darray.shape)
    check = check_frame(darray, positions, pattern="[^.0-9]")
    if check:
        total += int(n[0])
# print(f"Total: {total}")

num_adj_ast = []
for n in numbers:
    positions = frame_positions(
        start_position=n[1], length=n[2], array_shape=darray.shape)
    check = check_frame(darray, positions, pattern="[*]")
    fm = get_frame_matches(darray, positions, pattern="[*]")
    if check:
        num_adj_ast.append([n, fm[0][0]])
# print(f"Numbers adjacent to asterixes:\n{num_adj_ast}")

# Create df
df = pd.DataFrame.from_records(num_adj_ast, columns=['number', 'asterix_position'])
df[['number','number_start_position', 'length']] = pd.DataFrame(df.number.tolist(), index= df.index)
df = df.astype({'asterix_position': 'str'})
df = df.astype({'number': 'int'})

df = df.drop(['number_start_position', 'length'], axis=1)
#print(df.dtypes)
#print(df)

# add col from frequency of asterixes
df["count"] = df.groupby(["asterix_position"]).asterix_position.transform('count')
#data['CountSoldbyMonth']= data.groupby(['Date','Model']).TotalSoldCount.transform('count') 

# filter for just count == 2
df = df[df['count'] == 2] 

# group by asterix_position and multiply number values
df = df.groupby(['asterix_position']).prod()
#print(df)

# get sum of products
total = sum(df['number'])
print(total)


#### PART 2 test: 467835
#### PART 2 data: 75519888