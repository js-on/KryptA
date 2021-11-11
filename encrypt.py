#!/usr/bin/env python
def xor(out: str, key: str) -> str:
    res = ""
    for a,b in zip(out, key):
        if a == b:
            res += "0"
        else:
            res += "1"
    return res


boxes = open("sbox.csv", 'r').readlines()
S1 = boxes[0].strip().split(",")
S2 = boxes[1].strip().split(",")
BOX = {}
BOX[1] = {k: v for k,v in zip(sorted(S1), S1)}
BOX[2] = {k: v for k,v in zip(sorted(S2), S2)}
ROUNDS = 5
LENGTH = 5

KEY = "1011010101"

inp = "0101011001"
bits = inp

for _ in range(ROUNDS):
    first = bits[:5]
    print("first:", first)
    last = bits[5:]
    print("last:", last)
    first_mapped = BOX[1][first]
    print("first_mapped:", first_mapped)
    last_mapped = BOX[2][last]
    print("last_mapped:", last_mapped)
    output = first_mapped + last_mapped
    print("output:", output)
    bits = xor(output, KEY)
    print("bits:  ", bits)
    break
    # first = bits[:5]
    # last = bits[5:]
    # first_dec = int(first, 2)
    # last_dec = int(last, 2)
    # first_mapped = int(S1[first_dec], 2)
    # last_mapped = int(S2[last_dec], 2)
    # output = bin(first_mapped)[2:].zfill(5) + bin(last_mapped)[2:].zfill(5)
    # bits = xor(output, KEY)

print()
print("Key:   ", KEY)
print("Input: ", inp)
print("Output:", bits)