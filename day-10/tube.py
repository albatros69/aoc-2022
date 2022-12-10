#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

cycle = 1
instructions = { 'noop': 1, 'addx': 2 }
signal_strengths = []
next_poi = 20
X = 1

for l in lines:
    instr, *r = l.split()

    if cycle + instructions[instr] > next_poi:
        signal_strengths.append(next_poi * X)
        next_poi += 40

    if instr == 'addx':
        X += int(r[0])
    cycle += instructions[instr]

print("Part 1:", sum(signal_strengths))

cycle = 0
X = 1
screen = []
sprite = (X-1, X, X+1)

for l in lines:
    instr, *r = l.split()

    screen.extend('█' if (c%40) in sprite else ' ' for c in range(cycle, cycle+instructions[instr]))

    if instr == 'addx':
        X += int(r[0])
    sprite = (X-1, X, X+1)
    cycle += instructions[instr]

print("Part 2:")
for i in range(6):
    print(''.join(screen[40*i:40*(i+1)]))
