#! /usr/bin/env python

from itertools import product
import sys
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

map = defaultdict(lambda: '.')
for y,l in enumerate(lines):
    for x,m in enumerate(l):
        map[x+y*1j] = m


def neigh(z, adj=None):
    if adj is None:
        for delta in (1, -1, 1j, -1j, 1+1j, 1-1j, -1+1j, -1-1j):
            yield z+delta
    else:
        match adj:
            case 0: #'N'
                it = (-1j,1-1j,-1-1j)
            case 1: #'S'
                it = (1j,1+1j,-1+1j)
            case 2: #'W'
                it = (-1,-1+1j,-1-1j)
            case 3: #'E'
                it = (1,1+1j,1-1j)
        for delta in it:
            yield z+delta


directions = dict(zip(range(4), (-1j, 1j, -1, 1)))

def step(map, idx):
    new_map = defaultdict(lambda: '.')
    to_move = defaultdict(list)

    for z,m in list(map.items()):
        if m != '#':
            continue

        if all(map[n] == '.' for n in neigh(z)):
            new_map[z] = '#'
        else:
            for i in range(4):
                if all(map[n] == '.' for n in neigh(z, (i+idx)%4)):
                    to_move[z + directions[(i+idx)%4]].append(z)
                    break
            else:
                new_map[z] = '#'

    moved = 0
    for z, l in to_move.items():
        if len(l) == 1: # if the elve is alone on the new pos, it can move
            new_map[z] = '#'
            moved += 1
        elif len(l) > 1: # else they stay on their previous pos
            new_map.update({a: '#' for a in l})

    return new_map, moved


def empty_ground(map):
    EW = list(int(z.real) for z in map)
    NS = list(int(z.imag) for z in map)

    return sum(map[x+y*1j] == '.'
        for (x,y) in product(range(min(EW), max(EW)+1), range(min(NS), max(NS)+1))
    )


index_dir = 0
for _ in range(10):
    map, moved = step(map, index_dir)
    index_dir += 1

print("Part 1:", empty_ground(map))

while moved > 0:
    map, moved = step(map, index_dir)
    index_dir += 1

print("Part 2:", index_dir)
