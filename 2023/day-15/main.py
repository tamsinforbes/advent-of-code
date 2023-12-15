import re


filename = "data.txt"

f = open(filename, "r")
data = [item for item in f.readline().split(",")]

# hasha: Holiday ASCII String Helper algorithm (appendix 1A)." You turn to appendix 1A:
# Determine the (decimal) ASCII code for the current character of the string.
# Increase the current value by the ASCII code you just determined.
# Set the current value to itself multiplied by 17.
# Set the current value to the remainder of dividing itself by 256.

def hasha(string_to_hasha, current_value=0):
    # start_char = string_to_hasha[0]
    for s in string_to_hasha:
        current_value = (17 * (ord(s) + current_value)) % 256
    return current_value

def extract_label(s):
    """
    Extract the letters before the = or - in a string
    """
    label = re.split("([-=])", s)[0]
    return label


def hashamap(s, boxes):
    """
    Input:
        s: string to apply hashamap to
        boxes: dictionary of boxes of lenses, to use and uopdate
    Output:
        boxes: the dictionary of boxes now updated with the 
        outcome of applying the hashamap to the given string
    """
    split_s = re.split("([-=])", s)
    # extract the label and operation
    label, op = split_s[0], split_s[1]
    # get box number
    box = hasha(label)
    
    focal_length = None
    if op == "=":
        focal_length = int(split_s[2])
        if boxes.get(str(box)) and label in boxes.get(str(box))[0]:
            # The lens label is in the box, get label index
            label_index = boxes.get(str(box))[0].index(label)
            # Update the focal length with the current lens focal length
            boxes.get(str(box))[1][label_index] = focal_length
            print(f"Box {box} lens {label} updated with new focal length")
        elif boxes.get(str(box)):
            # If the box key exists there must be something in it so
            # append label and focal length to that
            boxes.get(str(box))[0].append(label)
            boxes.get(str(box))[1].append(focal_length)
            print(f"Box {box} updated with new lens {label}")
        else: # the box doesn't exist so create and add to it
            boxes[str(box)] = [[label], [focal_length]]
            print(f"Box {box} added with new lens {label}")

    elif op == "-": # Remove lens with matching label from box
        if boxes.get(str(box)) and label in boxes.get(str(box))[0]:
            # get index of label list in box that label matches; pop this and corresponding focal length
            label_index = boxes.get(str(box))[0].index(label)
            boxes.get(str(box))[0].pop(label_index)
            boxes.get(str(box))[1].pop(label_index)
            print(f"Box {box} updated to remove lens {label}")
        else:
            print(f"box {str(box)} empty; cannot remove lens {label}; do nothing")

    return boxes


def total_focusing_power(boxes):
    """
    Input:
        boxes: the dict of boxes of lenses
    Output:
        total_focusing_power: the sum of the focusing power of all the
        lenses in the box; focusing power is (1 + box) * slot * focal_length
    """
    total_focusing_power = 0
    for box in boxes:
        for lens, i in zip(boxes[box][0], range(len(boxes[box][0]))):
            total_focusing_power += (1 + int(box)) * (i +1) * boxes[box][1][i]
    return total_focusing_power


# -------------- PART 1 --------------
# Find the sum of the hashes of each string in the data
res = 0
for d in data:
    res += hasha(d)

print(f"Part 1 sum of hashes of strings in {filename}: {res}")
# Part 1 sum of hashes of strings in data.txt: 510273


# -------------- PART 2 ---------------
# something to do with boxes and different procedure for - or =


boxes = {"0": [[], []]} # init boxes
for d in data:
    boxes = hashamap(d, boxes)
print("\n", boxes, "\n")

total = total_focusing_power(boxes)
print(f"Part 2 total focusing power with {filename}: {total}")


############# NOTES ############
# If the operation character is a dash (-), go to the relevant box and remove 
# the lens with the given label if it is present in the box. Then, move any remaining
# lenses as far forward in the box as they can go without changing their order, filling
# any space made by removing the indicated lens. (If no lens in that box has the given
# label, nothing happens.)

# Store stuff in boxes for example like this
# Box 3: [pc 4] [ot 9] [ab 5]
# Store in dict as list of 2 corresponding lists of labels and focal lengthsa
# {"3": [["pc", "ot", "ab"],[4,9,5]]}

# If the operation character is an equals sign (=), it will be followed by a number 
# indicating the focal length of the lens that needs to go into the relevant box; be sure
# to use the label maker to mark the lens with the label given in the beginning of the step
# so you can find it later. There are two possible situations:

# If there is already a lens in the box with the same label, replace the old lens with the new lens:
# remove the old lens and put the new lens in its place, not moving any other lenses in the box.

# If there is not already a lens in the box with the same label, add the lens to the box immediately
# behind any lenses already in the box. Don't move any of the other lenses when you do this. If there
# aren't any lenses in the box, the new lens goes all the way to the front of the box.

# Now for the output dictionary of boxes calculate the focusing power

# To confirm that all of the lenses are installed correctly, add up the focusing power of all of the lenses.
# The focusing power of a single lens is the result of multiplying together:

# One plus the box number of the lens in question.
# The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
# The focal length of the lens.
# At the end of the above example, the focusing power of each lens is as follows:

# Box 0: [rn 1] [cm 2]
# Box 3: [ot 7] [ab 5] [pc 6]


# rn: 1 (box 0) * 1 (first slot) * 1 (focal length) = 1
# cm: 1 (box 0) * 2 (second slot) * 2 (focal length) = 4
# ot: 4 (box 3) * 1 (first slot) * 7 (focal length) = 28
# ab: 4 (box 3) * 2 (second slot) * 5 (focal length) = 40
# pc: 4 (box 3) * 3 (third slot) * 6 (focal length) = 72
# So, the above example ends up with a total focusing power of 145.
