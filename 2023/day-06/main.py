import numpy as np
import cmath
import math
import timeit

# -------- PART 1 --------
# Work out the number of ways of beating the existing distance record
# Input data comprises 
# Time: race time in milliseconds
# Distance: current record in millimeters for this race

# Determine the number of ways you could beat the record in each race. 
# What do you get if you multiply these numbers together?

filename = "data.txt"

f = open(filename, "r")
data = [line.strip("\n") for line in f.readlines()]
race_time = [int(v) for v in data[0].split(":")[1].split()]
record_distance = [int(v) for v in data[1].split(":")[1].split()]
print(race_time)
print(record_distance)

# ----- PART 1 - SIMPLE ------
# Equation for distance travelled
# R: race time, x: charge time, d: distance travelled
# d = (R - x)*x  ->  d = -x^2 + Rx

def distance(race_length, charge_time):
    R = race_length
    x = charge_time
    return -(x**2) + R*x

# setting one side equal to zero gives
# -x^2 + Rx -d = 0
# Then the inverse is given using quadratic formaula
# x = 0.5 (R +- sqrt(R^2 - 4*d))
def charge_time(race_length, distance):
    R = race_length
    d = distance
    root = (R**2 - 4*d)**0.5
    #root = cmath.sqrt(R**2 - 4*d)
    #root = math.sqrt(R**2 - 4*d)
    #return (0.5*(R + root), 0.5*(R-root))
    return min(0.5*(R + root), 0.5*(R-root))

# Max value of distance
# derivative of distance over charge time
# f(x) = -x^2 + Rx
# f'(x) = -2*x + R, solve for f'(x) = 0 gives
# x = 0.5 * R (half way)

# Find the number of ways to beat the record in each race
# Take the record distance and get the charge time that produces it
# Floor this to work out the number of integer charge times that can win

def get_ways(race_length, record_distance):
    R = race_length
    # get smallest charge time that produced that record distance
    ct = charge_time(race_length, record_distance)
    # find number of winning ways fom integer charge time
    w = (R + 1) - 2*(math.floor(ct)+1)
    return w

ways = []
for R, D in zip(race_time, record_distance):
    ways.append(get_ways(R, D))

print(f"Part 1 answer using {filename}: {np.prod(ways)}")

# ------- PART 2 -------
# Bad kernng: actually just a single race and record distance
# How many ways can you beat the record in this one much longer race?

single_race_time = int("".join([str(i) for i in race_time]))
single_record_distance = int("".join([str(i) for i in record_distance]))

print(f"{single_race_time}\n{single_record_distance}")
ways= get_ways(single_race_time, single_record_distance)

print(f"Part 2 answer using {filename}: {ways}")
