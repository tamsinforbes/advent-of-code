import re
import numpy as np

# -----------------------------------------
# -------------- PART ONE -----------------
# -----------------------------------------
# --- Day 4: Ceres Search ---
# "Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

# As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to 
# find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....
# The actual word search will be full of letters instead. For example:

# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX
# Take a look at the little Elf's word search. How many times does XMAS appear?

# Use re to search for all overlapping instances of XMAS in a string
# Then transpose the grid to get all the other directions to search in: 8 directions in total
# we, ew, ns, sn, ne, en, nw, wn
# Stuff can only overlap if reading backwards as well on the same line
# Find these by reversing the entire line instead 
# Have checked the data is square so can use numpy methods to get diagonals and anti-diagonals
line = "XMASXXXMASAMXSSSMMAASAMX"
# pattern = r"XMAS"
# res = re.findall(pattern=pattern, string=line)
# print(res)
# print(len(res))

def word_count(word: str, line: str):
  res = re.findall(pattern=word, string=line)
  return len(res)

line = "XMASXXXMASAMXSSSMMAASAMX"
res = word_count(word=r"XMAS", line=line)
# print(res)

# function to take a grid of letters and create list of strings for each
# line (horizontal, vertical, diagonals and their reverses)
# we, ew, ns, sn, ne, en, nw, wn
# assume read in from txt file to get W-E list of strings

def get_grid(filename):
  with open(filename) as f:
    lines = [line.rstrip() for line in f]
  return lines

# res = get_grid(filename="2024/day-04/test-2.txt")
# print(res)


def get_strings_in_all_8_directions(filename):
  with open(filename) as f:
    lines = [line.rstrip() for line in f]
  list_chars = [list(a) for a in lines]
  array_chars = np.array(list_chars, dtype=str)
  nrow = array_chars.shape[0]

  # Create lists of strings in all 8 directions
  # Horizontals we & ew
  we = lines
  ew = ["".join(a[::-1]) for a in list_chars]
  # Verticals ns & sn
  ns = ["".join(a) for a in np.transpose(array_chars).tolist()]
  sn = [a[::-1] for a in ns]
  # Main diagonals ne & en
  ne_char_lists = [array_chars.diagonal(a).tolist() for a in range(-nrow+1, nrow)]
  ne = ["".join(a) for a in ne_char_lists]
  en = [a[::-1] for a in ne]
  # Anti-diagonals nw & wn
  nw_char_lists = [np.fliplr(array_chars).diagonal(a).tolist() for a in range(-nrow+1, nrow)]
  nw = ["".join(a) for a in nw_char_lists]
  wn = [a[::-1] for a in nw]
  
  directions = [we, ew, ns, sn, ne, en, nw, wn]
  flattened_directions = [x for xs in directions for x in xs]

  return flattened_directions

def complete_wordsearch(filename, word):
  lines = get_strings_in_all_8_directions(filename=filename)
  total_count = 0
  for line in lines:
    total_count += word_count(word=word, line=line)
  return total_count


res = get_strings_in_all_8_directions(filename="2024/day-04/test-3.txt")
# print(res)


res = complete_wordsearch(filename="2024/day-04/test-2.txt", word=r"XMAS")
print(f"Day 4 Part 1 number of occurences of XMAS test 2 answer: {res}")
# Day 4 Part 1 number of occurences of XMAS test 2 answer: 5

res = complete_wordsearch(filename="2024/day-04/test-1.txt", word=r"XMAS")
print(f"Day 4 Part 1 number of occurences of XMAS test 1 answer: {res}")
# Day 4 Part 1 number of occurences of XMAS test 1 answer: 18

res = complete_wordsearch(filename="2024/day-04/data.txt", word=r"XMAS")
print(f"Day 4 Part 1 number of occurences of XMAS final answer: {res}")
# Day 4 Part 1 number of occurences of XMAS final answer: 2685 (correct)

# -----------------------------------------
# -------------- PART TWO -----------------
# -----------------------------------------

# Supposed to be finding X-MAS like this MAS or SAM in the form of an X
# M.S  M.M  S.M  S.S
# .A.  .A.  .A.  .A.
# M.S  S.S  S.M  M.M
# Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS 
# can be written forwards or backwards.
# Here's the same example from before, but this time all of the X-MASes have been kept instead:

# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........
# In this example, an X-MAS appears 9 times.

# So I think sliding window approach, checking every A
# And the 4 different possibilities
# M.S  M.M  S.M  S.S
# .A.  .A.  .A.  .A.
# M.S  S.S  S.M  M.M
# If A then get the corners in specific order say NW, NE, SE, SW
# If these are any of
# MSSM, MMSS, SMMS, SSMM
# Then we have an X-MAS
# No danger of double counting or overlapping as A only appears once in the pattern
