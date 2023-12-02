import re
import pandas as pd
import numpy as np

# -----------  Part 1  ------------
# The Elf would first like to know which games would have been possible if the bag
#  contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
# Determine which games would have been possible if the bag had been loaded with only 
# 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?

# max red = 12
# max green = 13
# max blue = 14

def possible_games(filename, max_red=12, max_green=13, max_blue=14):
    # read file
    f = open(filename, "r")
    games = [line.strip("\n") for line in f.readlines()]
    # init counter
    possible_games_count = 0
    sum_possible_games_ids = 0

    for g in games:
        x = g.split(": ")
        # Get game ID number
        game_id = int(x[0].split(" ")[1])
        # list of lists of number and colour for each draw in a game
        draws = [d.split(" ") for d in re.split("; |, ", x[1])]
        df = pd.DataFrame(draws, columns=["count","colour"])
        df["count"] = pd.to_numeric(df["count"])
        # get max of each colour for this game
        max_r = df[(df['colour'] == "red")]["count"].max()
        max_g = df[(df['colour'] == "green")]["count"].max()
        max_b = df[(df['colour'] == "blue")]["count"].max()

        # print(f"Game ID: {game_id}; Max red: {max_r}; Max green: {max_g}; Max blue: {max_b}")

        # Count possible games
        if (max_r > max_red or max_g > max_green or max_b > max_blue):
            #print(f"Game {game_id} impossible")
            continue
        else:
            #print(f"Game {game_id} possible")
            possible_games_count += 1
            sum_possible_games_ids += game_id

    return (possible_games_count, sum_possible_games_ids)

print(f"Test games output: Number of possible games: {possible_games('test.txt')[0]}; Sum of possible games IDs: {possible_games('test.txt')[1]}")
print(f"Final games output: Number of possible games: {possible_games('data.txt')[0]}; Sum of possible games IDs: {possible_games('data.txt')[1]}")

# -------------- Part 2 ----------------
# As you continue your walk, the Elf poses a second question: in each game you played, 
# what is the fewest number of cubes of each color that could have been in the bag to 
# make the game possible?

# Again consider the example games from earlier:

# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. 
# If any color had even one fewer cube, the game would have been impossible.
# Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.

# The power of a set of cubes is equal to the numbers of red, green, and blue
# cubes multiplied together. The power of the minimum set of cubes in game 1 
# is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up 
# these five powers produces the sum 2286.

# For each game, find the minimum set of cubes that must have been present. 
# What is the sum of the power of these sets?

# It looks at least 1 red, green, blue cube is drawn in each game
# "Elf shows you a small bag and some cubes which are either red, green, or blue."
# You might not draw any but there is at least 1.
# fewest number possible is simply the max of each colour in each game
# collect these max values and multiply together to get the "power" for each game
# then sum the powers

def power_sum_min_cubes_present(filename):
    # read file
    f = open(filename, "r")
    games = [line.strip("\n") for line in f.readlines()]
    # init counter
    sum_of_game_powers = 0

    for g in games:
        x = g.split(": ") # split at game id seperator
        # list of lists of number and colour for each draw in a game
        draws = [d.split(" ") for d in re.split("; |, ", x[1])]
        df = pd.DataFrame(draws, columns=["count","colour"])
        df["count"] = pd.to_numeric(df["count"])
        # get max of each colour for this game, swap nan with 1
        # there is at least 1 of each colour
        max_r = np.nan_to_num(df[(df['colour'] == "red")]["count"].max(), nan=1)
        max_g = np.nan_to_num(df[(df['colour'] == "green")]["count"].max(), nan=1)
        max_b = np.nan_to_num(df[(df['colour'] == "blue")]["count"].max(), nan=1)

        game_power = max_r * max_g * max_b
        sum_of_game_powers += game_power

    return sum_of_game_powers


print(f"Test games output: Sum of powers of games: {power_sum_min_cubes_present('test.txt')}")
print(f"Final games output: Sum of powers of games: {power_sum_min_cubes_present('data.txt')}")
