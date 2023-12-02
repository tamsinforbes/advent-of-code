import re
from word2number import w2n

# --------------- Part 1 ------------------
# The newly-improved calibration document consists of lines of text; 
# each line originally contained a specific calibration value that the Elves now need to recover. 
# On each line, the calibration value can be found by combining the first digit and the last digit 
# (in that order) to form a single two-digit number.

# For example:

# 1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet
# In this example, the calibration values of these four lines are 
# 12, 38, 15, and 77
# Adding these together produces 142.

# Consider your entire calibration document. What is the sum of all of the calibration values?

def get_calibration_sum(filename):
    f = open(filename, "r")
    data = [d.strip("\n") for d in f.readlines()]
    tens = []
    units = []
    for d in data:
        array = [int(s) for s in list(d) if s.isdigit()]
        tens.append(array[0])
        units.append(array[-1])
    return sum(tens) * 10 + sum(units)

print(f"Part 1 final answer: {get_calibration_sum('data.txt')}")

# -------------- Part 2 ---------------
# Actually some of the lines contain the numbers written out so include
# one, two, three, four, five, six, seven, eight, nine (not other numbers)
# as valid "digits".
# need to convert the string to numbers
# some numbers overlap, but this should be ok
# "xtwone3four" -> 2134 -> 24
# "7pqrstsixteen" -> 76 -> 76 (sixteen is not valid)
patterns = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

# Get first numbers
def get_first_numbers(filename, written_numbers):
    f = open(filename, "r")
    data = [d.strip("\n") for d in f.readlines()]
    first_num = []
    for d in data:
        pos_num = []
        # get numerical numbers
        match = re.search(r'\d', d)
        if match:
            pos_num.append(
                (match.start(), int(match.group()))
            )
        # get written numbers
        for p in written_numbers:
            match = re.search(p, d)
            if match:
                pos_num.append(
                    (match.start(), w2n.word_to_num(match.group()))
                )
        pos_num = sorted(pos_num)
        first_num.append(pos_num[0][1])
    #print("First numbers:", first_num)
    return first_num

# Get last numbers
def get_last_numbers(filename, written_numbers):
    f = open(filename, "r")
    data = [d.strip("\n") for d in f.readlines()]    
    last_num = []
    for d in data:
        pos_num = []
        # get numerical numbers
        match = re.search(r'\d', d[::-1])
        if match:
            pos_num.append(
                (match.start(), int(match.group()))
            )
        # get written numbers
        for p in written_numbers:
            match = re.search(p[::-1], d[::-1])
            if match:
                pos_num.append(
                    # (match.start(), match.group())
                    (match.start(), w2n.word_to_num(match.group()[::-1]))
                )
        pos_num = sorted(pos_num)
        # print(pos_num)
        last_num.append(pos_num[0][1])
    #print("Last numbers:", last_num)
    return last_num

patterns = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

first_numbers = get_first_numbers("test-2.txt", patterns)
last_numbers = get_last_numbers("test-2.txt", patterns)

# Get calibration figure

def adjusted_calibration_sum(filename, written_patterns):
    tens = get_first_numbers(filename, written_patterns)
    units = get_last_numbers(filename, written_patterns)
    return 10 * sum(tens) + sum(units)

# adjusted_calibration_sum("test-2.txt", patterns)

# Part 2 final answer
print(f"Part 2 final answer: {adjusted_calibration_sum('data.txt', patterns)}")
