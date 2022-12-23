#! /usr/bin/env python

from __future__ import annotations
from dataclasses import dataclass, field
import sys
import re
from collections import defaultdict
from typing import Tuple


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

map = defaultdict(lambda: ' ')
max_x, max_y = 0, 0
for y,l in enumerate(lines[:-2]):
    for x,m in enumerate(l):
        map[x+y*1j] = m
    max_x, max_y = max(max_x, x), max(max_y, y)

path = [ int(m) if m.isdigit() else m for m in re.findall(r'([0-9]+|[LR])', lines[-1])]

def print_map(m):
    for y in range(max_y+1):
        print(''.join(m[x+y*1j] for x in range(max_x+1)))


def turn(s, mov):
    pos, dir = s
    return (pos, (dir+1)%4) if mov == 'R' else (pos, (dir-1)%4)

def move(pos, dir):
    if dir == 0: # >
        return pos + 1
    elif dir == 1: # v
        return pos + 1j
    elif dir == 2: # <
        return pos - 1
    elif dir == 3: # ^
        return pos - 1j

def next_tile_part1(s):
    pos, dir = s
    next_pos = move(pos, dir)

    if map[next_pos] == ' ':
        # Wrap around the map
        if dir == 0: # >
            next_pos = min((k for k in (next_pos-x for x in range(max_x+1)) if map[k]!=' '), key=lambda z: z.real)
        elif dir == 1: # v
            next_pos = min((k for k in (next_pos-y*1j for y in range(max_y+1)) if map[k]!=' '), key=lambda z: z.imag)
        elif dir == 2: # <
            next_pos = max((k for k in (next_pos+x for x in range(max_x+1)) if map[k]!=' '), key=lambda z: z.real)
        elif dir == 3: # ^
            next_pos = max((k for k in (next_pos+y*1j for y in range(max_y+1)) if map[k]!=' '), key=lambda z: z.imag)

    return next_pos, dir


start = min((k for k,v in map.items() if v == '.'), key=lambda z: (z.imag, z.real))
# map[start] = 'S'
# print_map(map) ; print()

status = (start, 0) # >
# new_map = map.copy()
# directions = ">v<^"
for instr in path:
    pos, dir = status
    # new_map[pos] = directions[dir]

    if isinstance(instr, int):
        for _ in range(instr):
            pos, dir = next_tile_part1(status)
            if map[pos] == '#':
                break
            # new_map[pos] = directions[dir]
            status = pos, dir
    else:
        status = turn(status, instr)

pos, dir = status
# new_map[pos] = 'E'
# print_map(new_map)
print("Part 1:", int(1000*(pos.imag+1) + 4*(pos.real+1)) + dir)


@dataclass
class Face():
    origin: complex
    N: Tuple[Face, str] = None
    E: Tuple[Face, str] = None
    S: Tuple[Face, str] = None
    W: Tuple[Face, str] = None
    submap: dict = field(default_factory = dict)

# We cut the map into the 6 faces of the cube
# You will have to adapt this to your input if needed
# Could be generalized relatively easily (detecting empty space)
faces = {
    1: Face( 50     ), 2: Face(100     ), 3: Face( 50+ 50j),
    4: Face(  0+100j), 5: Face( 50+100j), 6: Face(  0+150j),
}

for y in range(0,50):
    for x in range(0,50):
        z = x+y*1j
        for face in faces.values():
            face.submap[z] = map[z+face.origin]

# Hardcoding the faces transition of my input
# You will have to adapt this to your input if needed
# Generalizing this could be tricky...
# See r/adventofcode on Reddit for some hints!
faces[1].N = (faces[6], 'W')
faces[1].E = (faces[2], 'W')
faces[1].S = (faces[3], 'N')
faces[1].W = (faces[4], 'W')

faces[2].N = (faces[6], 'S')
faces[2].E = (faces[5], 'E')
faces[2].S = (faces[3], 'E')
faces[2].W = (faces[1], 'E')

faces[3].N = (faces[1], 'S')
faces[3].E = (faces[2], 'S')
faces[3].S = (faces[5], 'N')
faces[3].W = (faces[4], 'N')

faces[4].N = (faces[3], 'W')
faces[4].E = (faces[5], 'W')
faces[4].S = (faces[6], 'N')
faces[4].W = (faces[1], 'E')

faces[5].N = (faces[3], 'S')
faces[5].E = (faces[2], 'E')
faces[5].S = (faces[6], 'E')
faces[5].W = (faces[4], 'E')

faces[6].N = (faces[4], 'S')
faces[6].E = (faces[5], 'S')
faces[6].S = (faces[2], 'N')
faces[6].W = (faces[1], 'N')

# max_x = 49; max_y = 49
# print_map(faces[4].submap)


def adj_tile(pos: complex):
    if pos.imag <= 0:
        return 'N'
    elif pos.imag >= 49:
        return 'S'
    elif pos.real >= 49:
        return 'E'
    elif pos.real <= 0:
        return 'W'

ident = lambda z: z
# Gives you the function to apply to the pos to switch from one edge
# to the other, plus the new direction
# Should be generic enough
transitions = {
    ('N', 'S'): (ident, 3), ('S', 'N'): (ident, 1),
    ('E', 'W'): (ident, 0), ('W', 'E'): (ident, 2),
    ('N', 'N'): (ident, 1), ('S', 'S'): (ident, 3),
    ('E', 'E'): (ident, 2), ('W', 'W'): (ident, 0),
    ('N', 'E'): (lambda z: 49+(49-z.real)*1j, 2), ('N', 'W'): (lambda z: z.real*1j        , 0),
    ('S', 'E'): (lambda z: 49+z.real*1j     , 2), ('S', 'W'): (lambda z: (49-z.real)*1j   , 0),
    ('E', 'N'): (lambda z: 49-z.imag        , 1), ('W', 'N'): (lambda z: z.imag           , 1),
    ('E', 'S'): (lambda z: z.imag+49j       , 3), ('W', 'S'): (lambda z: (49-z.imag)+49j, 3),
}

def next_tile_part2(s, face: Face):
    pos, dir = s
    next_pos = move(pos, dir)

    if next_pos in face.submap:
        return (next_pos, dir), face

    side = adj_tile(pos)
    new_face, new_side = getattr(face, side)
    f, new_dir = transitions[side, new_side]
    return (f(pos), new_dir), new_face


# new_map = map.copy()
# new_map[faces[1].origin] = "S"
# directions = ">v<^"
status = (0, 0), faces[1]

for instr in path:
    (pos, dir), face = status
    # new_map[pos+face.origin] = directions[dir]

    if isinstance(instr, int):
        for _ in range(instr):
            (pos, dir), face = next_tile_part2(*status)
            if face.submap[pos] == '#':
                break
            # new_map[pos+face.origin] = directions[dir]
            status = (pos, dir), face
    else:
        status = turn((pos, dir), instr), face

(pos, dir), face = status
pos = pos+face.origin
# new_map[pos] = 'E'
# print_map(new_map)
print("Part 2:", int(1000*(pos.imag+1) + 4*(pos.real+1)) + dir)
