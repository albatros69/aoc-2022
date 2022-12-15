#! /usr/bin/env python

from __future__ import annotations
from dataclasses import dataclass
import sys
import re
from collections import defaultdict
from itertools import product

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


@dataclass
class Pt():
    x: int
    y: int

    def __add__(self, other: Pt):
        return Pt(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pt):
        return Pt(self.x - other.x, self.y - other.y)

    def dist(self, other: Pt):
        tmp = self - other
        return abs(tmp.x) + abs(tmp.y)

    def as_tuple(self):
        return self.x, self.y


@dataclass
class Interval():
    start: int
    end: int

    def length(self):
        return self.end - self.start + 1

    def union(self, other):
        if other is None:
            return self
        elif self.end < other.start or other.end < self.start:
            if self.start-other.end == 1 or other.start-self.end==1:
                return [Interval(min(self.start, other.start), max(self.end, other.end))]
            return [self, other]
        else:
            if self.start <= other.start <= self.end:
                return [Interval(self.start, max(self.end, other.end))]
            elif self.start <= other.end <= self.end:
                return [Interval(min(self.start, other.start), self.end)]
            else:
                if self.start <= other.start:
                    return [self]
                else:
                    return [other]

    def difference(self, other):
        if other is None or self.end < other.start or other.end < self.start:
            return [self]
        else:
            res = []
            if self.start < other.start <= self.end:
                res.append(Interval(self.start, other.start-1))
            if self.start <= other.end < self.end:
                res.append(Interval(other.end+1, self.end))
            return res


@dataclass
class Sensor():
    pos: Pt
    beacon: Pt

    def detection_area(self):
        d = self.pos.dist(self.beacon)

        for i,j in product(range(-d, d+1), repeat=2):
            cand = self.pos + Pt(i,j)
            if self.pos.dist(cand) <= d:
                yield cand


    def pt_roi(self, y):
        d = self.pos.dist(self.beacon)

        if abs(self.pos.y - y) > d:
            return None

        x1 = abs(y - self.pos.y) - d + self.pos.x
        x2 = d - abs(y - self.pos.y) + self.pos.x
        return Interval(x1, x2)


# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
re_line = re.compile(r'Sensor at x=(?P<Sx>[0-9-]+), y=(?P<Sy>[0-9-]+): '\
    r'closest beacon is at x=(?P<Bx>[0-9-]+), y=(?P<By>[0-9-]+)')
sensors = []
for l in lines:
    tmp = re_line.match(l)
    sensor = { a: int(tmp.group(f'S{a}')) for a in ('x', 'y') }
    beacon = { a: int(tmp.group(f'B{a}')) for a in ('x', 'y') }

    sensors.append(Sensor(Pt(**sensor), Pt(**beacon)))

# def print_map():
#     min_x = min(p[0] for p in map)
#     min_y = min(p[1] for p in map)
#     max_x = max(p[0] for p in map)
#     max_y = max(p[1] for p in map)

#     for j in range(min_y, max_y+1):
#         print(''.join(map[i,j] for i in range(min_x, max_x+1)))

# map = defaultdict(lambda: '.')
# for sensor in sensors:
#     for p in sensor.detection_area():
#         map[p.as_tuple()] = '#'

# for sensor in sensors:
#     map[sensor.pos.as_tuple()] = 'S'
#     map[sensor.beacon.as_tuple()] = 'B'

# row_of_interest = 10
row_of_interest = 2000000
tmp = sorted(
    filter(lambda x: x is not None, (sensor.pt_roi(row_of_interest) for sensor in sensors)),
    key=lambda x: x.start)

def reduce_part1(interval_list):
    if len(interval_list) <= 1:
        return interval_list
    else:
        a,b, *tail = interval_list
        tmp = a.union(b)
        if len(tmp) == 1:
            return reduce_part1(tmp + tail)
        else:
            return tmp[:1] + reduce_part1(tmp[1:] + tail)

sensors_roi = set(sensor.pos.as_tuple() for sensor in sensors if sensor.pos.y==row_of_interest)
beacons_roi = set(sensor.beacon.as_tuple() for sensor in sensors if sensor.beacon.y==row_of_interest)

# print_map()
print("Part 1:", max(x.length() for x in reduce_part1(tmp)) - len(sensors_roi) - len(beacons_roi))

# maxi = 20
maxi = 4000000
for y in range(maxi+1):
    result = [Interval(0, maxi)]
    for i in filter(lambda x: x is not None, (sensor.pt_roi(y) for sensor in sensors)):
        tmp = []
        for t in result:
            tmp.extend(t.difference(i))
        result = tmp
        if not result:
            break

    if len(result) == 1 and result[0].length() == 1:
        break
    # if y%1000 == 0:
    #     print(y, end='\r')

print("Part 2:", result[0].start*4000000+y)
