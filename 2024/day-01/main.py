import numpy as np
import pandas as pd


# -----------------------------------------
# -------------- PART ONE -----------------
# -----------------------------------------
# There's just one problem: by holding the two lists up side by side (your puzzle input), it quickly becomes clear that the lists aren't very similar.
#  Maybe you can help The Historians reconcile their lists?

# For example:

# 3   4
# 4   3
# 2   5
# 1   3
# 3   9
# 3   3

# In the example list above, the pairs and distances would be as follows:

# The smallest number in the left list is 1, and the smallest number in the right list is 3. The distance between them is 2.
# The second-smallest number in the left list is 2, and the second-smallest number in the right list is another 3. The distance between them is 1.
# The third-smallest number in both lists is 3, so the distance between them is 0.
# The next numbers to pair up are 3 and 4, a distance of 1.
# The fifth-smallest numbers in each list are 3 and 5, a distance of 2.
# Finally, the largest number in the left list is 4, while the largest number in the right list is 9; these are a distance 5 apart.
# To find the total distance between the left list and the right list, add up the distances between all of the pairs you found. In the example above, this is 2 + 1 + 0 + 1 + 2 + 5, a total distance of 11!

# Your actual left and right lists contain many location IDs. What is the total distance between your lists?

# Ingest data in 2 separate lists
# order each list
# stick in an array/df, find the diff between each col and sum to get the total diff

def sum_of_absolute_diffs_from_ordered_lists(filename):
  with open(filename, 'r') as data:
      x = []
      y = []
      for line in data:
          p = line.split()
          x.append(float(p[0]))
          y.append(float(p[1]))

  result = int(sum(abs(np.sort(np.array(x))-np.sort(np.array(y)))))
  return result

test_result = sum_of_absolute_diffs_from_ordered_lists(filename="2024/day-01/test-1.txt")
print(f"Part 1 test answer: {test_result}")

part_1_answer = sum_of_absolute_diffs_from_ordered_lists(filename="2024/day-01/data.txt")
print(f"Part 1 final answer: {part_1_answer}")

# Part 1 final answer: 1938424



# -----------------------------------------
# -------------- PART TWO -----------------
# -----------------------------------------
# This time, you'll need to figure out exactly how often each number from the left list appears in the right list. 
# Calculate a total similarity score by adding up each number in the left list after multiplying it by the number of
# times that number appears in the right list.

# Here are the same example lists again:

# 3   4
# 4   3
# 2   5
# 1   3
# 3   9
# 3   3

# For these example lists, here is the process of finding the similarity score:

# The first number in the left list is 3. It appears in the right list three times, so the similarity score increases by 3 * 3 = 9.
# The second number in the left list is 4. It appears in the right list once, so the similarity score increases by 4 * 1 = 4.
# The third number in the left list is 2. It does not appear in the right list, so the similarity score does not increase (2 * 0 = 0).
# The fourth number, 1, also does not appear in the right list.
# The fifth number, 3, appears in the right list three times; the similarity score increases by 9.
# The last number, 3, appears in the right list three times; the similarity score again increases by 9.
# So, for these example lists, the similarity score at the end of this process is 31 (9 + 4 + 0 + 0 + 9 + 9).

# Once again consider your left and right lists. What is their similarity score?

# The way described above requires repeatedly counting in the right list
# This is not necessary: I propose this formula:
# For each list find the frequency of each number; 
# left list: 3:3, 4:1, 2:1, 1:1
# right list: 4:1, 3:3, 5:1, 9:1
# then join on the number value then multiply number by freq in each list and sum the results
# num L-freq R-freq res
#   1      1      0   0
#   2      1      0   0
#   3      3      3  27
#   4      1      1   4
#   5      0      1   0
#   9      0      1   0

# Total = 27 + 4 = 31

def get_similarity_score(filename):
  with open(filename, 'r') as data:
    x = []
    y = []
    for line in data:
        p = line.split()
        x.append(int(p[0]))
        y.append(int(p[1]))
  
  # create dfs of counts, make values the key or index so as to concat on this axis
  unique, counts = np.unique(np.array(x), return_counts=True)
  left_df = pd.DataFrame(data={"key": unique, "left_count": counts}).set_index("key")
  unique, counts = np.unique(np.array(y), return_counts=True)
  right_df = pd.DataFrame(data={"key": unique, "right_count": counts}).set_index("key")

  # full union join dfs
  df = pd.concat([left_df, right_df], axis=1)
  df = df.fillna(0)
  df["score"] = df.index * df["left_count"] * df["right_count"]
  similarity_score = int(sum(df["score"]))

  return similarity_score

test_score = get_similarity_score(filename="2024/day-01/test-1.txt")
print(f"Part 2 test similarity score: {test_score}")
# Part 2 test similarity score: 31

score = get_similarity_score(filename="2024/day-01/data.txt")
print(f"Part 2 final answer similarity score: {score}")
# Part 2 final answer similarity score: 22014209