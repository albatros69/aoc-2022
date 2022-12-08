#! /usr/bin/env python

import sys
from itertools import product

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

forest = {}
for y,l in enumerate(lines):
    for x,tree in enumerate(l):
        forest[x,y] = int(tree)
nb_rows = y+1
nb_cols = x+1

def is_visible(x,y):
    return x == 0 or x == nb_cols-1 or y == 0 or y == nb_rows-1 or \
        all(forest[x,y] > forest[x,i] for i in range(y)) or \
        all(forest[x,y] > forest[x,i] for i in range(y+1, nb_rows)) or \
        all(forest[x,y] > forest[i,y] for i in range(x)) or \
        all(forest[x,y] > forest[i,y] for i in range(x+1, nb_cols))

print("Part 1:", sum(is_visible(x,y) for (x,y) in product(range(nb_rows), range(nb_cols))))

def scenic_score(x,y):
    result = 1
    for i in reversed(range(y)):
        if forest[x,i] >= forest[x,y]:
            result *= abs(y-i)
            break
    else:
        result *= abs(y)

    for i in range(y+1, nb_rows):
        if forest[x,i] >= forest[x,y]:
            result *= abs(y-i)
            break
    else:
        result *= abs(y-nb_rows+1)

    for i in reversed(range(x)):
        if forest[i,y] >= forest[x,y]:
            result *= abs(x-i)
            break
    else:
        result *= abs(x)

    for i in range(x+1, nb_cols):
        if forest[i,y] >= forest[x,y]:
            result *= abs(x-i)
            break
    else:
        result *= abs(x-nb_cols+1)

    return result

print("Part 2:", max(scenic_score(x,y) for (x,y) in product(range(nb_rows), range(nb_cols))))
