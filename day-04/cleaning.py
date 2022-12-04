#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

result = 0
pairs = []
for l in lines:
    (beg1, end1), (beg2, end2) = (tuple(int(x) for x in a.split('-')) for a in l.split(','))
    pairs.append(((beg1, end1), (beg2, end2)))
    if (beg1 <= beg2 <= end1 and beg1 <= end2 <= end1) \
        or (beg2 <= beg1 <= end2 and beg2 <= end1 <= end2):
        result += 1
print("Part 1:", result)

result = 0
for (beg1, end1), (beg2, end2) in pairs:
    if beg1 <= beg2 <= end1 or beg1 <= end2 <= end1 \
        or beg2 <= beg1 <= end2 or beg2 <= end1 <= end2:
        result += 1
print("Part 2:", result)

