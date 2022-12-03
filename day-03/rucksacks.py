#! /usr/bin/env python

import sys
import itertools

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def priority(item):
    if item.islower():
        return ord(item)-ord('a')+1
    else:
        return ord(item)-ord('A')+27

result = 0
for rucksack in lines:
    mid = len(rucksack)//2
    c1, c2 = rucksack[:mid], rucksack[mid:]
    commons = set(a for a in c1 if a in c2)
    result += sum(priority(a) for a in commons)
print("Part 1:", result)

def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

result = 0
for r1,r2,r3 in grouper(3, lines):
    result += sum(priority(a) for a in set(r1)&set(r2)&set(r3))
print("Part 2:", result)

