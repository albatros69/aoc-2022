#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

datastream = lines[0]
for i in range(4, len(datastream)):
    marker = datastream[i-4:i]
    if len(set(marker)) == 4:
        break
print("Part 1:", i, marker)

for i in range(14, len(datastream)):
    marker = datastream[i-14:i]
    if len(set(marker)) == 14:
        break
print("Part 2:", i, marker)
