#! /usr/bin/env python

from __future__ import annotations
from collections import deque
from dataclasses import dataclass, astuple
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

@dataclass(frozen=True)
class Droplet():
    x: int
    y: int
    z: int

    def __getitem__(self, item):
        return astuple(self)[item]

    def __add__(self, other):
        return Droplet(self.x+other[0], self.y+other[1], self.z+other[2])

    def norme(self):
        return max(abs(self.x), abs(self.y), abs(self.z))

    def neighbors(self):
        for pt in ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)):
            yield self+pt


droplets = set()
for l in lines:
    droplets.add(Droplet(*(int(a) for a in l.split(','))))
max_norme = max(d.norme() for d in droplets)

result = 0
for p in droplets:
    for neigh in p.neighbors():
        if neigh not in droplets:
            result += 1

print("Part 1:", result)


INSIDE = set()
OUTSIDE = set()
def is_internal(droplet: Droplet):
    global INSIDE, OUTSIDE
    if droplet in INSIDE:
        return True
    if droplet in OUTSIDE:
        return False

    queue = deque((droplet,))
    already_seen = set()

    while queue:
        d = queue.popleft()
        if d in already_seen or d in droplets:
            continue

        if d.norme() > max_norme:
            OUTSIDE |= already_seen
            return False

        already_seen.add(d)
        queue.extend(n for n in d.neighbors() if n not in already_seen)

    INSIDE |= already_seen
    return True

result = 0
for p in droplets:
    for neigh in p.neighbors():
        if not is_internal(neigh):
            result += 1

print("Part 2:", result)
