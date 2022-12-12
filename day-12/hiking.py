#! /usr/bin/env python

import sys
from heapq import heappop, heappush


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

grid = {}
for j,l in enumerate(lines):
    for i,e in enumerate(l):
        grid[i,j] = e


def height(square):
    if square == 'S':
        return ord('a')
    elif square == 'E':
        return ord('z')
    else:
        return ord(square)


def walk(q):
    already_seen = {}
    while q:
        steps, x, y = heappop(q)

        if (x,y) in already_seen and already_seen[x,y] <= steps:
            continue

        if grid[x,y] == 'E':
            return steps

        already_seen[x,y] = steps
        for (new_x, new_y) in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            try:
                if height(grid[new_x,new_y]) - height(grid[x,y]) <= 1:
                    heappush(q, (steps+1, new_x, new_y))
            except KeyError:
                continue

    return None


queue = [ (0, i, j) for (i,j) in grid if grid[i,j]=='S' ]
print("Part 1:", walk(queue))


queue = [ (0, i, j) for (i,j) in grid if height(grid[i,j])==height('a') ]
print("Part 2:", walk(queue))
