import numpy as np
# -----------------------------------------
# -------------- PART ONE -----------------
# -----------------------------------------
# The unusual data (your puzzle input) consists of many reports, one report per line. 
# Each report is a list of numbers called levels that are separated by spaces. For example:

# 7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9
# This example data contains six reports each containing five levels.

# The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems 
# can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report 
# only counts as safe if both of the following are true:

# The levels are either all increasing or all decreasing.
# Any two adjacent levels differ by at least one and at most three.
# In the example above, the reports can be found safe or unsafe by checking those rules:

# 7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
# 1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
# 9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
# 1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
# 8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
# 1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
# So, in this example, 2 reports are safe.

# Analyze the unusual data from the engineers. How many reports are safe?

# So find the diffs between each level moving right across the report
# The diffs must either be all +1s, +2s, +3s or all -1s, -2s, -3s
# The diffs, d, must be either all 1<=d<=3 or -3<=d<=-1
# So all between -3 and -1 or all between 1 and 3 

def count_safe_reports_homogeneous_shape(filename):
  with open(filename) as f:
      reports = []
      for line in f:
          reports.append(np.array([int(i) for i in line.split()]))

  # Uses array of 1D arrays (assumes all arrays are same length)
  # Else you get inhomogeneous shape error
  a = np.array([np.diff(report) for report in reports])
  decreasing = ((-3 <= a) & (a <= -1))
  increasing = ((1 <= a) & (a <= 3))

  decreasing_safe_count = sum(np.all(decreasing, axis=1))
  increasing_safe_count = sum(np.all(increasing, axis=1))

  return decreasing_safe_count + increasing_safe_count

test_1_safe_count = count_safe_reports_homogeneous_shape(filename="2024/day-02/test-1.txt")
print(f"Part 1 test homogeneous data (unlike actual data!); count of safe reports: {test_1_safe_count}")
# Part 1 test homogeneous data (unlike actual data!); count of safe reports: 2
# Test data is a homogeneous shape so can create an array of arrays, actual data isn't homogeneous!

def count_safe_reports(filename):
  with open(filename) as f:
      reports = []
      for line in f:
          reports.append(np.array([int(i) for i in line.split()]))

  # Use list of 1D arrays
  diffs = [np.diff(report) for report in reports]
  safe_count = 0
  for d in diffs:
    if np.all((-3 <= d) & (d <= -1)):
      safe_count += 1
    elif np.all((1 <= d) & (d <= 3)):
      safe_count += 1
    else:
      continue

  return safe_count

test_safe_count = count_safe_reports(filename="2024/day-02/test-2.txt")
print(f"Part 1 test inhomogeneous shaped data; count of safe reports: {test_safe_count}")
# Part 1 test inhomogeneous shaped data; count of safe reports: 2

part_1_answer = count_safe_reports(filename="2024/day-02/data.txt")
print(f"Day 2 Part 1 number of safe reports final answer: {part_1_answer}")
# Day 2 Part 1 number of safe reports final answer: 421