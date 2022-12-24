#! /usr/bin/env python

from functools import cache
import sys
from itertools import product
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

mvt = { '>': (1,0), '<': (-1,0), 'v': (0,1), '^': (0,-1), }
blizzards_ini = []
max_y = len(lines)
for y,l in enumerate(lines[1:-1]):
    max_x = len(l)
    for x,w in enumerate(l[1:-1]):
        if w in mvt:
            blizzards_ini.append(((x+1,y+1), mvt[w]))

all_pos = set(product(range(1, max_x-1), range(1, max_y-1)))
start, end = (1,0), (max_x-2, (max_y-1))
all_pos |= set((start, end))
all_pos = frozenset(all_pos)


def add_t(u,v):
    return tuple(a+b for (a,b) in zip(u,v))

def dist(u,v):
    return sum(abs(a-b) for (a,b) in zip(u,v))

def next_pos(z, dir):
    x,y = add_t(z, dir)
    return (x-1)%(max_x-2)+1, (y-1)%(max_y-2)+1

@cache
def blizzard_move(m):
    new = frozenset((next_pos(z, d), d) for (z,d) in m)
    return new, all_pos - frozenset(p[0] for p in new)


def explore(start, end, valley):
    queue = [ (dist(start, end), start, 0, frozenset(valley)) ]
    already_seen = set()
    while queue:
        _, curr_pos, curr_min, curr_map = heappop(queue)

        if curr_pos == end:
            return curr_min, curr_map
        if (curr_pos, curr_map) in already_seen:
            continue
        already_seen.add((curr_pos, curr_map))

        new_map, free = blizzard_move(curr_map)
        if curr_pos in free and (curr_pos, new_map) not in already_seen:
            # no blizzard entering our position: we can stay
            heappush(queue, (dist(curr_pos, end)+curr_min+1, curr_pos, curr_min+1, new_map))
        for delta in mvt.values():
            x,y = add_t(curr_pos, delta)
            if (x,y) in free and ((x,y), new_map) not in already_seen:
                heappush(queue, (dist((x,y), end)+curr_min+1, (x,y), curr_min+1, new_map))

    return -1, frozenset()


result = []
blizz = blizzards_ini
for goals in ((start, end), (end, start), (start, end)):
    minute, blizz = explore(*goals, blizz)
    result.append(minute)
print("Part 1:", result[0])
print("Part 2:", sum(result))

