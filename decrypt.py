#!/usr/bin/env python3
from typing import KeysView


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

boxes = open("sbox.csv", 'r').readlines()
S1 = boxes[0].strip().split(",")
S2 = boxes[1].strip().split(",")
BOX = {}
BOX[1] = {k: v for k,v in zip(sorted(S1), S1)}
BOX[2] = {k: v for k,v in zip(sorted(S2), S2)}

ROUNDS = 5
LENGTH = 5

KEY = "1011010101"
outp = "0110101001"
bits = outp

for _ in range(ROUNDS):
    bits_xor = xor(bits, KEY)
    print("bits_xor:", bits_xor)
    first = bits[:5]
    print("first:", first)
    last = bits[5:]
    print("last:", last)
    first_mapped = get_key(BOX[1], first)
    print("first_mapped:", first_mapped)
    last_mapped = get_key(BOX[2], last)
    print("last_mapped:", last_mapped)
    bits = first_mapped + last_mapped
    print("bits:", bits)
    break

print()
print("Key:   ", KEY)
print("Input: ", outp)
print("Output:", bits)