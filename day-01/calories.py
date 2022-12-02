#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

elves = []
accu = 0
for l in lines:
    if l:
        accu += int(l)
    else:
        elves.append(accu)
        accu = 0

if accu:
    elves.append(accu)

elves.sort()
print("Part 1:", elves[-1])
print("Part 2:", sum(elves[-3:]))
