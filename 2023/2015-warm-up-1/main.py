f = open("test-0-1.txt", "r")
print(f.read())

# python3 <name-of-file>

test_files = [
    "test-0-1.txt",
    "test-0-1.txt",
    "test-3-1.txt",
    "test-3-2.txt",
    "test-3-3.txt",
    "test--1-1.txt",
    "test--1-2.txt",
    "test--3-1.txt",
    "test--3-2.txt",
]

final = "directions.txt"

# -----------  Part 1: find what floor santa ends up on --------------

def compute_floor(filename):
    floor = 0
    print("Start floor: ", floor)
    with open(filename, "r") as f:
        while True:
            c = f.read(1)
            if not c:
                print("End of file")
                break
            if c == "(":
                floor += 1
            elif c == ")": # when I had just else here I got 73 for the answer, with elif get 74; else must miss the final ( +1
                floor -= 1
        print("End floor:", floor)

# for test in test_files:
#     compute_floor(test)

# compute_floor(final)

# ------------ Part 2: find the character position of the first time Santa is on level -1 ------------
# This must occur on the way down, so at a )
# convert the direction into a list of floor numbers
# and find position od first coccurence of -1 in list of floors visited
# NB index from 1 (not 0! so add 1 to final output)

# use test files with -1 in
test_files = [
    "test-3-3.txt",
    "test--1-1.txt",
    "test--1-2.txt",
    "test--3-1.txt",
    "test--3-2.txt",
]

def get_floor_visit_order(filename):
    floor_numbers = []
    floor = 0
    print("Start floor: ", floor)
    with open(filename, "r") as f:
        while True:
            c = f.read(1)
            if not c:
                print("End of file")
                break
            if c == "(":
                floor += 1
            elif c == ")": # when I had just else here I got 73 for the answer, with elif get 74; else must miss the final ( +1
                floor -= 1
            floor_numbers.append(floor)
        print(floor_numbers)
        print("Position of first instance of -1:", floor_numbers.index(-1) + 1) # add 1 to account for python indexing from 0
        print("End floor:", floor)

for test in test_files:
    print("Start test: ", test)
    get_floor_visit_order(test)

get_floor_visit_order(final)
# Position of first instance of -1: 1795
# End floor: 74
