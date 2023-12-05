# ------------- PART 1 -------------
# --- Day 3: Perfectly Spherical Houses in a Vacuum ---
# Santa is delivering presents to an infinite two-dimensional grid of houses.

# He begins by delivering a present to the house at his starting location, and then an elf at the North Pole 
# calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^),
# south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

# However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off,
# and Santa ends up visiting some houses more than once. How many houses receive at least one present?

# For example:

# > delivers presents to 2 houses: one at the starting location, and one to the east.
# ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
# ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.

# Translate directions into list of coordinate locations
# set of this list is the set of unique houses visited

filename = "data.txt"
f = open(filename, "r")
directions = [line.strip("\n") for line in f.readlines()] 
directions = list(directions[0])

# Use (x,y) for [East-West, North-South], [col, row]
coordinates = [(0,0)]
x = 0
y = 0
for d in directions:
    if d == "^":
        y += 1
        coordinates.append((x, y))
    elif d == "v":
        y += -1
        coordinates.append((x, y))
    elif d == ">":
        x += 1
        coordinates.append((x, y))
    elif d == "<":
        x += -1
        coordinates.append((x, y))

print(f"Part 1: Number of unique houses visited: {len(set(coordinates))}")

# Part 1 data answer: 2081
# Part 2 test answer: 11

# --------------- PART 2 --------------
# Now Sant ans Robo-Santa take turns delivering the presents, santa takes the odd numbered directions and 
# Robo-santa the even numbered directiosn

def houses_visited(directions):
    """
    Input: directions: a list of individual chars ^v<> indicating a move one unit N, S, E, W
    Output: houses_visited: integer number of unique houses visited
    """
    coordinates = [(0,0)]
    x = 0
    y = 0
    for d in directions:
        if d == "^":
            y += 1
            coordinates.append((x, y))
        elif d == "v":
            y += -1
            coordinates.append((x, y))
        elif d == ">":
            x += 1
            coordinates.append((x, y))
        elif d == "<":
            x += -1
            coordinates.append((x, y))
    return set(coordinates)

#print(houses_visited(directions))

# Split the full directions into santa directions and robo-santa directions
santa = directions[::2]
robo = directions[1::2]

# print(directions)
# print(santa)
# print(robo)

santa_visits = houses_visited(santa)
robo_visits = houses_visited(robo)

# They may still visit the same house so need the union of the two sets to remove duplicates 
print(f"Part 2: Number of unique houses visited by Santa and Robo-Santa: {len(santa_visits.union(robo_visits))}")

# Part 2 answer data: 2341
# Part 2 test answer: 10