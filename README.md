### WIP!
Executables to create **bad** s-boxes for learning crypt analysis.

Current selection:

`01110,00100,10110,01100,10101,01111,10100,00000,01011,00111,11011,10001,00010,01010,11000,10000,11010,10111,11101,10010,11111,11100,00101,00001,01001,01000,00011,11001,00110,10011,11110,01101`

`00100,11001,01110,01010,10111,01101,01100,01011,11000,10001,00111,11011,00011,00110,00000,11010,10000,10011,00001,01000,00010,01111,11110,10010,11111,11100,01001,11101,10100,10110,00101,10101`

### Usage
Use `./cryptnim` on *nix systems, `.\cryptnim.exe` on Windows.
Generate *x* s-boxes of size *y* (bitsize) in *z* rounds with the `--loop|-l` parameter:<br>
`./cryptnim -l 500 4 5` ... Creates 4 s-boxes of size 5bit in 500 iterations

Test s-boxes from CSV file `sbox.csv` (in the same directory) and show proximity tables with the `--test|-t` parameter:<br>
`./cryptnim -t`

### Files
- `cryptpy.py`: Working but slow! Usage same as above (only long parameters!)
- `cryptcpp.cpp`: Faster but not working as it should... Find the bug and you'll get a cookie! Same usage as above.
- `cryptnim.nim`: Works as expected. See usage above. Compile with nim v1.6.0: `nim c -r -d:release -d:danger --opt:speed cryptnim.nim`

Cross-compile to windows: `nim c -d:mingw --cpu:amd64 -d:danger -d:release --opt:speed cryptnim.nim`

Cross-compile to linux: `nim c --cpu:arm --os:linux cryptnim.nim`

### Weight
Quantity: Count all values not equal to mean value

Quality:  Sum of all deviations ^ 2

Variance: Sum of variances higher than threshold (± 6 from mean value)

Dominant: Dominant proximity (most ocurring variant value)

### Benchmark
There's none, STFU and do it yourself.