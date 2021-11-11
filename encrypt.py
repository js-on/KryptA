#!/usr/bin/env python
def xor(out: str, key: str) -> str:
    res = ""
    for a,b in zip(out, key):
        if a == b:
            res += "0"
        else:
            res += "1"
    return res

KEYS = [
    "1010110100",
    "1001010101",
    "0101001010",
    "1101010110",
    "0001100101"
]

boxes = open("sbox.csv", 'r').readlines()
S1 = boxes[0].strip().split(",")
S2 = boxes[1].strip().split(",")
BOX = {}
BOX[1] = {k: v for k,v in zip(sorted(S1), S1)}
BOX[2] = {k: v for k,v in zip(sorted(S2), S2)}
ROUNDS = 5
LENGTH = 5

print("Encrypt with the best encryption you'll ever see!")
inp = input("Input: ")
bits = inp

for i in range(ROUNDS):
    KEY = KEYS[i]
    first = bits[:5]
    last = bits[5:]
    first_mapped = BOX[1][first]
    last_mapped = BOX[2][last]
    output = first_mapped + last_mapped
    bits = xor(output, KEY)

print()
print("Key:   ", KEY)
print("Input: ", inp)
print("Output:", bits)