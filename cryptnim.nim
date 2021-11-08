from os import commandLineParams
from algorithm import sort
from math import `^`, isPowerOfTwo, round, log2
from random import shuffle, randomize
import parseopt
import strutils
from times import now, `-`
import tables


var BIT_SIZE: int
var BOILERPLATE: seq[string]
let THRESHOLD: int = 6

type
    Rating* = object
        quality*, quantity*, variance*: int
        box: seq[string]

## convert string sequence to int sequence
proc convertBinSequence(s: seq[string]): seq[int] =
    var res: seq[int]
    result = res
    for i in s:
        result.add(parseBinInt(i))

## Get highest value from table
proc maxTable(t: Table[int, int], ignore: int): string =
    var key = 0
    var val = 0
    for (k, v) in t.pairs:
        if v > val and k != ignore:
            key = k
            val = v
    return "val " & $key & " appears " & $val & " times"

## Calculate linear approximation for given input to output on s-box
proc linearApprox(s: seq[int], input_bit: int, output_bit: int): int =
    result = 0
    for ii in 0..(s.len()-1):
        var masked_input = ii and input_bit
        var masked_output = s[ii] and output_bit
        if (masked_input.toBin(BIT_SIZE).count("1") - masked_output.toBin(BIT_SIZE).count("1")) mod 2 == 0:
            inc result

## Check if s-box contains only unique elements
## Check if length of s-box is power of 2
proc validateSbox(s: string): bool =
    var tmp = s.split(",")
    sort(tmp)
    for i in 0..(tmp.len()-2):
        if tmp[i] == tmp[i+1]:
            return false
    if isPowerOfTwo(tmp.len()):
        result = true
    else:
        result = false

## Analyze box and return weight; print proximity table if debug is set to true
proc analyzeBox(s: seq[string], debug: bool = false): Rating {.discardable.} =
    var box = convertBinSequence(s)
    var quality: int = 0
    var quantity: int = 0
    var variance: int = 0
    var domApprox = initTable[int, int]()
    if debug:
        stdout.write "    | "
        for i in 0..(len(s)-1):
            stdout.write intToStr(i).align(3, ' ') & " "
        echo ""
        echo " " & "-".repeat(s.len()*4+4)
    for row in 0..(s.len()-1):
        if debug:
            stdout.write intToStr(row).align(3, ' ') & " | "
        for col in 0..(s.len()-1):
            var res = linearApprox(box, row, col)
            if debug:
                var highlight = ""
                if res == 16:
                    highlight = "\e[1;31m"
                elif res <= 16-THRESHOLD or res >= 16 + THRESHOLD:
                    inc variance
                    highlight = "\e[1;32m"
                    # if not domApprox.hasKey(res):
                    #     domApprox[res] = 1
                    # else:
                    #     inc domApprox[res]
                # if res != 16:
                if not domApprox.hasKey(res):
                    domApprox[res] = 1
                else:
                    inc domApprox[res]
                stdout.write highlight & ($res).align(3, ' ') & "\e[00m " 
            if res != (s.len() div 2):
                quality += abs((s.len() div 2) - res) ^ 2
                inc quantity
        if debug:
            echo ""
    if debug:
        echo "S-Box:          " & s.join(",")
        echo "Quality:        " & $quality
        echo "Quantity:       " & $quantity
        echo "Variance:       " & $variance
        echo "Mean dominance: " & maxTable(domApprox, -1)
        echo "  └──► without 0. row and 0. column: " & $(s.len() * s.len() - quantity - 62) & " times"
        echo "High dominance: " & maxTable(domApprox, 16)
        echo "Complete table: "
        var key_store = ""
        var val_store = ""
        for (k, v) in domApprox.pairs:
            key_store.add(($k).align(3, ' ') & " ")
            val_store.add(($v).align(3, ' ') & " ")
        echo "Value   | " & key_store
        echo "Appears | " & val_store
        echo ""
    result = Rating(quality: quality, quantity: quantity, variance: variance, box: s)

## read x-boxes from csv and run analysis
proc testCSV() =
    var content = readFile("sbox.csv").splitLines()
    BIT_SIZE = int(float(content[0].len()))
    for i in 0..(content.len()-1):
        var line = content[i]
        if validateSbox(line):
            analyzeBox(line.split(","), true)
        else:
            echo "Please check box S" & $i & " for duplicate elements or invalid length"
    quit(0)

## TODO: returne shuffled stuff
proc randomSbox(): seq[string] =
    result = BOILERPLATE
    shuffle(result)

proc initBoilerplate(): seq[string] =
    var tmp: seq[string]
    result = tmp
    for i in 0..(2^BIT_SIZE-1):
        result.add(toBin(i, BIT_SIZE))

proc progress(pos: int, length: int) =
    var r = int(round(50/length*float(pos)))
    stdout.write "Progress: [" & "#".repeat(r) & " ".repeat(50-r) & "] " & $pos & "/" & $length & "\r"

proc loopBox(args: seq[string]) =
    var iterations = parseInt(args[0])
    var count = parseInt(args[1])
    BIT_SIZE = parseInt(args[2])
    BOILERPLATE = initBoilerplate()
    var ratings: seq[Rating]
    for i in 0..(count-1):
        ratings.add(Rating(quality: 0, quantity: 0, variance: 0, box: @[]))
    let t1 = now()
    for i in 0..iterations:
        progress(i, iterations)
        var box = randomSbox()
        var tmp = analyzeBox(box, false)
        for i in 0..(count-1):
            var rating = ratings[i]
            if tmp.quality > rating.quality or tmp.variance > rating.variance:
                ratings[i] = tmp
                break
    let t2 = now()
    for i in 0..(count-1):
        echo "\n"
        echo "S" & $i
        analyzeBox(ratings[i].box, true)
        # echo "Quality:  " & $ratings[i].quality
        # echo "Quantity: " & $ratings[i].quantity
        echo "S-Box:    " & ratings[i].box.join(",") & "\n"
    echo "\nRuntime: " & $(t2 - t1)
    quit(0)

proc main() =
    randomize()
    var p = initOptParser(commandLineParams())
    while true:
        p.next()
        case p.kind
        of cmdEnd: break
        of cmdShortOption, cmdLongOption:
            if p.val == "":
                if p.key == "t" or p.key == "test":
                    testCSV()
                elif p.key == "l" or p.key == "loop":
                    loopBox(p.remainingArgs())
        of cmdArgument: discard

if isMainModule:
    main()
