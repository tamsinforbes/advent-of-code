#-------------- PART 1 ---------------
# Find the total wrapping paper square feet required 
# Square feet required is surface area plus smallest side area

filename = "test.txt"
f = open(filename, "r")
data = [d.strip("\n") for d in f.readlines()]
#print(data)

total_square_feet = 0

for d in data:
    s = d.split("x")
    s = sorted([eval(side) for side in s])
    required_area = 3*s[0]*s[1] + 2*(s[0]*s[2] + s[1]*s[2])
    total_square_feet += required_area
print(f"Total wrapping paper: {total_square_feet}")

# PART 1 test data: 8206
# PART 1 final data: 1606483

#-------------- PART 2 ---------------
# Find length of ribbon required
# perimeter of the smallest face to wrap
# plus a length equal to the cubic feet volume for the bow
# For example:
# A present with dimensions 2x3x4 requires 2+2+3+3 = 10 feet of ribbon
# to wrap the present plus 2*3*4 = 24 feet of ribbon for the bow, for 
# a total of 34 feet.

total_ribbon_length = 0
for d in data:
    s = d.split("x")
    s = sorted([eval(side) for side in s])
    smallest_side_perimeter = 2*(s[0] + s[1])
    volumne = s[0] * s[1] * s[2]
    ribbon = smallest_side_perimeter + volumne
    total_ribbon_length += ribbon
print(f"Total ribbon: {total_ribbon_length}")

# PART 1 test data: 19746
# PART 1 final data: 3842356