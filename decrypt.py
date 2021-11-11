#!/usr/bin/env python3
def xor(out: str, key: str) -> str:
    res = ""
    for a,b in zip(out, key):
        if a == b:
            res += "0"
        else:
            res += "1"
    return res

def get_key(box: dict, val: str) -> str:
    for k,v in box.items():
        if v == val:
            return k

KEYS = [
    "1010110100",
    "1001010101",
    "0101001010",
    "1101010110",
    "0001100101"
][::-1]

boxes = open("sbox.csv", 'r').readlines()
S1 = boxes[0].strip().split(",")
S2 = boxes[1].strip().split(",")
BOX = {}
BOX[1] = {k: v for k,v in zip(sorted(S1), S1)}
BOX[2] = {k: v for k,v in zip(sorted(S2), S2)}

ROUNDS = 5
LENGTH = 5

print("Decrypt our fancy shit!")
outp = input("Input: ")
bits = outp

for i in range(ROUNDS):
    KEY = KEYS[i]
    bits_xor = xor(bits, KEY)
    first = bits_xor[:5]
    last = bits_xor[5:]
    first_mapped = get_key(BOX[1], first)
    last_mapped = get_key(BOX[2], last)
    bits = first_mapped + last_mapped

print()
print("Key:   ", KEY)
print("Input: ", outp)
print("Output:", bits)