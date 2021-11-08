# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 12:12:03 2021

@author: jasch
"""

from typing import Tuple
import random
import sys

def _help():
    print("Give one of the following parameters:")
    print("\t-test   :: Test s-boxes store as CSV in S1.txt / S2.txt")
    print("\t-loop x :: Loop through X s-boxes to find best possible in this run")

def progress(pos: int, length: int):
    print(f"Progress: [{round(50/length*pos)*'#'}{(50-round(50/length*pos))*' '}] {pos}/{length}", end='\r')

def linearApprox(s: list, input_bit: int, output_bit: int) -> str:
    total = 0
    for ii in range(len(s)):
        input_masked = ii & input_bit
        output_masked = s[ii] & output_bit
        if (bin(input_masked).count("1") - bin(output_masked).count("1")) % 2 == 0:
            total += 1
    result = total - len(s)//2
    result = str(len(s)//2 + result)
    return result


def test_sbox(s, debug: bool = False) -> Tuple[int, int]:
    s = [int("0b" + i, 2) for i in s]
    quality = 0
    quantity = 0
    if debug:
        sys.stdout.write("    | ")
        for i in range(len(s)):
            sys.stdout.write(str(i).rjust(3) + " ")
        print("")
        print(" " + "-"*(len(s)*4+4))
    for row in range(len(s)):
        if debug:
            sys.stdout.write(str(row).rjust(3) + " | ")
        for col in range(len(s)):
            res = linearApprox(s, row, col)
            if debug:
                sys.stdout.write(res.rjust(3) + " ")
            if res != str(16):
                quality += abs(int(res))**2
                quantity += 1
        if debug:
            print("")
    if debug:
        print("Quality:", quality)
        print("Quantity:", quantity)
    return (quality, quantity)
    

def s1(fname: str = "") -> list:
    if fname == "":
        s1: list = [str(bin(i))[2:].zfill(5) for i in range(32)] 
        random.shuffle(s1)
    else:
        line = open(fname, 'r').readlines()[0]
        s1 = [i.strip() for i in line.split(",")]
    return s1

def s2(fname: str = "") -> list:
    if fname == "":
        s2: list = [str(bin(i))[2:].zfill(5) for i in range(32)] 
        random.shuffle(s2)
    else:
        line = open(fname, 'r').readlines()[0]
        s2 = [i.strip() for i in line.split(",")]
    return s2

def key() -> str:
    key: list = ''.join([str(random.choice([0, 1])) for _ in range(10)])
    return key