import numpy as np
# ------------ PART 1 -------------
# Get next value in a sequence
# Diff to next values in seq is same or higher (absolute value)
# Sequences do not go up and down

filename = "data.txt"

f = open(filename, "r")
data = np.array([[int(v) for v in line.strip("\n").split()] for line in f.readlines()])

def get_next(seq):
    output = []
    diffs = np.diff(seq)
    while not np.all(diffs==0):
        output.append(diffs[-1])
        diffs = np.diff(diffs)

    return seq[-1] + sum(output)

next_values = []
for d in data:
    next_values.append(get_next(d))

print(f"Part 1 solution with {filename}: Sum of next values in sequences: {sum(next_values)}")

# 1786100822 INCORRECT: too high! while loop condition: sum(diffs) == 0; which could happen before they were all zero
# 950144101 INCORRECT: too low! tried np.any(diffs) - not sure why
# 1782868781 CORRECT used while not np.all(diff==0)

#--------- PART 2 ----------
# Get the previous value in each sequence

seq = [1,2,5,-3]

st = seq[0]
for s in seq[1:]:
    st = s - st
    print(st)

def get_previous(seq):
    output = []
    diffs = np.diff(seq)
    while not np.all(diffs==0):
        output.append(diffs[0])
        diffs = np.diff(diffs)
    
    if len(output) == 1:
        return seq[0] - output[0]
    else:        
        rev = output[::-1]
        subtractor = rev[0]
        for r in rev[1:]:
            subtractor = r - subtractor
        previous = seq[0] - subtractor
        return previous


previous_values = []
for d in data:
    previous_values.append(get_previous(d))
#print(f"Previous values: {previous_values}")
print(f"Part 2 solution with {filename}: Sum of previous values in sequences: {sum(previous_values)}")
