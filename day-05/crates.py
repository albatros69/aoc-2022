#! /usr/bin/env python

import sys
from copy import deepcopy

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

tmp = []
moves = []
for l in lines:
    if l.startswith('move'):
        moves.append(tuple(int(a) for a in l.split()[1::2]))
    elif l:
        tmp.append(l)

nb_stacks = int(tmp[-1].split()[-1])
stacks_ori = [ [] for _ in range(nb_stacks) ]
for row in tmp[-1::-1]:
    for i in range(nb_stacks):
        crate = row[4*i+1]
        if crate.isupper():
            stacks_ori[i].append(row[4*i+1])

stacks = deepcopy(stacks_ori)
for (c, s, e) in moves:
    for _ in range(c):
        stacks[e-1].append(stacks[s-1].pop())

print("Part 1:", ''.join(s[-1] for s in stacks))

stacks = deepcopy(stacks_ori)
for (c, s, e) in moves:
    stacks[e-1].extend(stacks[s-1][-c:])
    stacks[s-1] = stacks[s-1][:-c]

print("Part 2:", ''.join(s[-1] for s in stacks))
