import re
import numpy as np

# -----------------------------------------
# -------------- PART ONE -----------------
# -----------------------------------------
# The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. 
# All of the instructions have been jumbled up!

# It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y),
# where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly,
# mul(123,4) would multiply 123 by 4.

# However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored,
# even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

# For example, consider the following section of corrupted memory:

# xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
# Only the four highlighted sections are real mul instructions. 
# mul(2,4) mul(5,5) mul(11,8) mul(8,5)
# Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

# This is a regex problem
# Data is split over 6 lines, emanually inspected that each line doesn't not split a valid instruction
# Can read and process each line separately

def get_corrupted_instructions(filename):
  with open(filename) as f:
    lines = [line.rstrip('\n') for line in f]
  return lines

def extract_valid_pattern(lines: list, pattern: str):
  valid_muls = []
  for line in lines:
    result = re.findall(pattern=pattern, string=line)
    valid_muls.append(result)
  flattened_valid_muls = [x for xs in valid_muls for x in xs]
  return flattened_valid_muls

def mul(mulstring:str):
  """
  Function to extract the numbers and multiple from a
  mul(123,34) type instruction.
  Returns product as int.
  """
  m1, m2 = mulstring[4:-1].split(",")
  return int(m1) * int(m2)


def run_part_one(filename, pattern):
  instructions = get_corrupted_instructions(filename=filename)
  mulstrings = extract_valid_pattern(lines=instructions, pattern=pattern)

  products = []
  for mulstring in mulstrings:
    products.append(mul(mulstring=mulstring))


  return sum(np.array(products))


res = run_part_one(filename="2024/day-03/test-1.txt", pattern=r"mul\(\d{1,3},\d{1,3}\)")
print(f"Day 3 Part 1 test answer: {res}")

res = run_part_one(filename="2024/day-03/data.txt", pattern=r"mul\(\d{1,3},\d{1,3}\)")
print(f"Day 3 Part 1 final answer: {res}")

# 189527826
# 32215984 is too low!!! I had forgotten to flatten the valid muls list so I was only processing the last
# line of instructions in the data

# -----------------------------------------
# -------------- PART TWO -----------------
# -----------------------------------------
# As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact.
# If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

# There are two new instructions you'll need to handle:

# The do() instruction enables future mul instructions.
# The don't() instruction disables future mul instructions.
# Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

# For example:

# xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
# This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are
# disabled because there is a don't() instruction before them. The other mul instructions function normally, including the
# one at the end that gets re-enabled by a do() instruction.

# This time, the sum of the results is 48 (2*4 + 8*5).

# Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?

# So only count mul() instrustions between a LHS do() and RHS don't()
# Input needs to be all one string

# New test-2 data: sum of valid products is 96
# xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
# xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

# Should give same resuult as test-3 data which is just test-2 in one line: sum of valid products is 96
# xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

# lines = get_corrupted_instructions(filename="2024/day-03/test-2.txt")
# print(lines)
# delimiter = ""
# corrupted_string = delimiter.join(lines)
# print(corrupted_string)

# pattern = r"(mul\(\d{1,3},\d{1,3}\))|(don't\(\))|(do\(\))"
# res = re.findall(pattern=pattern, string=corrupted_string)
# print(res)
# print(type(res[0]))

def extract_enabled_mul_instructions(instructions: list):
  enable = True
  enabled_muls = []
  for i in instructions:
    if enable and i[0] == "m":
      enabled_muls.append(i)
    elif enable and i == "don't()":
      enable = False
    elif not enable and i == "do()":
      enable = True

  return enabled_muls


def run_part_two(filename, pattern):
  # Get data and concat to one string
  lines = get_corrupted_instructions(filename=filename)
  delimiter = ""
  corrupted_string = delimiter.join(lines)

  # Extract all the mul() don't() do() valid pattern matches
  # This returns a list of tuples with empty string where no match found
  res = re.findall(pattern=pattern, string=corrupted_string)
  # Flatten to list of strings, dropping empty strings
  valid_instructions = [x for xs in res for x in xs if x]

  # Get just the enabled mul() instructions
  enabled_mul_instructions = extract_enabled_mul_instructions(valid_instructions)

  # Find products
  products = []
  for mulstring in enabled_mul_instructions:
    products.append(mul(mulstring=mulstring))

  return sum(np.array(products))

res = run_part_two(
  filename="2024/day-03/test-2.txt",
  pattern=r"(mul\(\d{1,3},\d{1,3}\))|(don't\(\))|(do\(\))"
)
print(f"Day 3 Part 2 test 2 answer: {res}")


res = run_part_two(
  filename="2024/day-03/test-3.txt",
  pattern=r"(mul\(\d{1,3},\d{1,3}\))|(don't\(\))|(do\(\))"
)
print(f"Day 3 Part 2 test 3 answer: {res}")

res = run_part_two(
  filename="2024/day-03/data.txt",
  pattern=r"(mul\(\d{1,3},\d{1,3}\))|(don't\(\))|(do\(\))"
)
print(f"Day 3 Part 2 final answer: {res}")