#! /usr/bin/env python

import sys
from collections import defaultdict
from math import floor

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def move_head(pos: complex, dir: str):
    match dir:
        case 'R':
            mov = 1
        case 'L':
            mov = -1
        case 'U':
            mov = 1j
        case 'D':
            mov = -1j

    return pos + mov

def sign(a: float):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0

def move_tail(pos_head: complex, pos_tail: complex):
    if floor(abs(pos_head-pos_tail)) > 1:
        mov = complex(sign(pos_head.real - pos_tail.real), sign(pos_head.imag - pos_tail.imag))
        return pos_tail + mov
    return pos_tail


head = 0j
tail = 0j
grid = defaultdict(int)
grid[0,0] += 1

for (mov, cpt) in (l.split() for l in lines):
    for _ in range(int(cpt)):
        head = move_head(head, mov)
        tail = move_tail(head, tail)
        grid[tail.real, tail.imag] += 1

print("Part 1:", sum(grid[i,j]>0 for (i,j) in grid))

rope = [ 0j, ] * 10
grid = defaultdict(int)
grid[0,0] += 1

for (mov, cpt) in (l.split() for l in lines):
    for _ in range(int(cpt)):
        rope[0] = move_head(rope[0], mov)
        for i in range(1, 10):
            rope[i] = move_tail(rope[i-1], rope[i])
        grid[rope[-1].real, rope[-1].imag] += 1

print("Part 2:", sum(grid[i,j]>0 for (i,j) in grid))
