# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 11:42:15 2021
@author: Jakob Schaffarczyk
@date: 01.11.2021
"""

import sbox
import sys

# def xor(a, b) -> str:
#     return str(int(a) ^ int(b))

# x: list = [str(bin(i))[2:].zfill(5) for i in range(32)]
# s1: list = sbox.s1("S1.txt")
# s1 = "00000,01000,10000,11000,00001,01001,10001,11001,00010,01010,10010,11010,00011,01011,10011,11011,00100,01100,10100,11100,00101,01101,10101,11101,00110,01110,10110,11110,00111,01111,10111,11111".split(",")
# s2: list = sbox.s2("S2.txt")
# key: str = sbox.key()
# in_bits: str = str(bin(ord("J")))[2:].zfill(10)

# bits1: str = in_bits[:5]
# bits2: str = in_bits[5:]

# print("in_bits:", in_bits)
# print("bits1:", bits1)
# print("bits2:", bits2)
# print("key:", key)
# print("S1:", ','.join(s1))
# print("S2:", ','.join(s2))

if len(sys.argv) == 1:
    sbox._help()
    sys.exit(1)
elif sys.argv[1] == "-test":
    s1 = "000,010,100,110,011,111,101,001".split(",")#sbox.s1("S1.txt")
    s2 = "111,011,010,101,000,001,100,110".split(",")#sbox.s2("S2.txt")
    sbox.test_sbox(s1, debug=True)
    # sbox.test_sbox(s2, debug=False)

elif sys.argv[1] == "-loop":
    if len(sys.argv) != 3:
        print("You need to pass a range like `-loop 50`")
        sys.exit(1)
    else:
        try:
            rng = int(sys.argv[2])
            if rng < 1:
                print("Range must be a positive number")
                sys.exit(1)
        except:
            print("Range must be a valid number")
            sys.exit(1)
    
    data1 = {
        "quality": 0,
        "quantity": 0,
        "box": None,
    }
    data2 = {
        "quality": 0,
        "quantity": 0,
        "box": None,
    }
    for i in range(rng):
        sbox.progress(i, rng)
        s1 = sbox.s1()
        quality, quantity = sbox.test_sbox(s1)
        if quality > data1["quality"] or quantity > data1["quantity"]:
            data1["quality"] = quality
            data1["quantity"] = quantity
            data1["sbox"] = s1
        elif quality > data2["quality"] or quantity > data2["quantity"]:
            data2["quality"] = quality
            data2["quantity"] = quantity
            data2["sbox"] = s1
    print("\n")
    print("S1")
    print("Quality: ", data1["quality"])
    print("Quantity:", data1["quantity"])
    print("S-Box:", ','.join(data1["sbox"]))
    print("\n")
    print("S1")
    print("Quality: ", data2["quality"])
    print("Quantity:", data2["quantity"])
    print("S-Box:", ','.join(data2["sbox"]))
        
else:
    sbox._help()
    sys.exit(1)

# out_bits = []

# sx: str = bits1
# index: int = x.index(sx)
# sy: str = s1[index]
# out_bits.append(sy)
# print(f"S1(x) = {sx} → {sy}")

# sx: str = bits2
# index: int = x.index(sx)
# sy: str = s2[index]
# out_bits.append(sy)
# print(f"S2(x) = {sx} → {sy}")

# out_bits = ''.join(out_bits)
# out_bits_plus_key = ""
# for i in range(10):
#     out_bits_plus_key += xor(out_bits[i], key[i])

# print(out_bits)
# print(out_bits_plus_key)