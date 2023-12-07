import hashlib

# --- Day 4: The Ideal Stocking Stuffer ---
# Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts
# for all the economically forward-thinking little girls and boys.

# To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least
# five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given
# below) followed by a number in decimal. To mine AdventCoins, you must find Santa 
# the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

# For example:

# If your secret key is abcdef, the answer is 609043, because the MD5 hash of
# abcdef609043 starts with five zeroes (000001dbbfa...),and it is the lowest such
# number to do so.
# If your secret key is pqrstuv, the lowest number it combines with to make an MD5
# hash starting with five zeroes is 1048970; that is, the MD5 hash of pqrstuv1048970
# looks like 000006136ef....

# Your puzzle input is ckczppom.

test = "abcdef"
test_answer = "609043"
test_input = test+test_answer
data = "ckczppom"

result = hashlib.md5(b"abcdef609043")
#print(result.hexdigest())

result = hashlib.md5(test_input.encode())
# result = hashlib.md5(b"")
#print(result.hexdigest())

# def mine_advent_coin(secret_key, start_guess=100000, lead_zeroes=5):
#     """
#     Input: 
#         secret_key: string
#         start_guess: starting number
#         lead_zeroes: number of lead zeroes required in hexadecimal hash
#     """

#     test_input = secret_key + str(start_guess)
#     start_result = hashlib.md5(test_input.encode())
#     hex = start_result.hexdigest()

#     if hex[0:5] == "00000":
#         print(f"found it")
#         print(hex)
#     else:
#         print("sad")
    
#     while hex[0:5] != "00000":
#         test_input = secret_key + str(start_guess+=1)
#         result = hashlib.md5(test_input.encode())
#         hex = result.hexdigest()
#     return result.hexdigest()

# check = mine_advent_coin(secret_key="abcdef", start_guess=609041)
# print(check)