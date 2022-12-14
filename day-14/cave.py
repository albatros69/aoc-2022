#! /usr/bin/env python

from collections import defaultdict
from itertools import product
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def sign(a):
    if a >= 0:
        return 1
    return -1

def next_pos(x,y):
    return (x,y+1), (x-1,y+1), (x+1,y+1)


class Cave():
    map: dict
    start = 500,0
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    count_units: int

    def __init__(self, lines) -> None:
        self.map = defaultdict(lambda: '.')
        self.count_units = 0
        self.min_x, self.min_y, self.max_x, self.max_y = self.start *2
        for l in lines:
            self.draw_rock(l)

    def __repr__(self):
        return '\n'.join(
            ''.join(self.map[x,y] for x in range(self.min_x-1, self.max_x+2))
            for y in range(self.min_y-1, self.max_y+1))

    def draw_line(self, start, end):
        t,u = start
        v,w = end
        self.min_x = min(self.min_x, t, v) ; self.max_x = max(self.max_x, t, v)
        self.min_y = min(self.min_y, u, w) ; self.max_y = max(self.max_y, u, w)
        for (i,j) in product(range(t, v+sign(v-t), sign(v-t)), range(u, w+sign(w-u), sign(w-u))):
            self.map[i,j] = '#'

    def draw_rock(self, line):
        prev = None
        for pt in line.split(' -> '):
            current = tuple(int(a) for a in pt.split(','))
            if prev is None:
                prev = current
                continue

            self.draw_line(prev, current)
            prev = current


    def add_sand_part1(self, pos):
        if pos[1] > self.max_y:
            return False

        result = False
        for new_pos in next_pos(*pos):
            if self.map[new_pos] == '.':
                result = self.add_sand_part1(new_pos)
                break
        else:
            if self.map[pos] == '.':
                self.map[pos] = 'o'
                self.count_units += 1
                return True

        return result

    def add_sand_part2(self, pos):
        self.min_x = min(self.min_x, pos[0])
        self.max_x = max(self.max_x, pos[0])

        if pos[1] > self.max_y:
            return False

        result = False
        for new_pos in next_pos(*pos):
            if self.map[new_pos] == '.':
                result = self.add_sand_part2(new_pos)
                break
        else:
            if self.map[pos] == '.':
                self.map[pos] = 'o'
                self.count_units += 1
                return True

        if not result and self.map[pos] == '.':
            self.map[pos] = 'o'
            self.count_units += 1
            return True

        return result


cave = Cave(lines)

# print(cave)
# print(cave.add_sand(cave.start))
# print(cave)
# print(cave.add_sand(cave.start))
while cave.add_sand_part1(cave.start):
    pass
print("Part 1:", cave, cave.count_units, sep='\n')

cave.max_y += 1
while cave.add_sand_part2(cave.start):
    pass
print("Part 2:", cave, "#"*(cave.max_x-cave.min_x+3), cave.count_units, sep='\n')
