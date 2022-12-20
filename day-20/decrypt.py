#! /usr/bin/env python

import sys
from collections import deque

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def solve(f, k=1, cpt=1):
    mixed = deque(((i,k*v) for i,v in enumerate(f)), len(f))
    init_order = tuple(mixed)

    for _ in range(cpt):
        for a,v in init_order:
            i = mixed.index((a,v))
            mixed.rotate(-i)
            mixed.popleft()
            mixed.rotate(-v)
            mixed.appendleft((a,v))

    return mixed


file = [int(a) for a in lines]
zero = (file.index(0), 0)
cycle = len(file)

decrypted_file = solve(file)
offset = decrypted_file.index(zero)
coordinates = [ decrypted_file[(i+offset)%cycle][1] for i in (1000, 2000, 3000) ]
print("Part 1:", sum(coordinates))

decrypted_file = solve(file, 811589153, 10)
offset = decrypted_file.index(zero)
coordinates = [ decrypted_file[(i+offset)%cycle][1] for i in (1000, 2000, 3000) ]
print("Part 2:", sum(coordinates))
