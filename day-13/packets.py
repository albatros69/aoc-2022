#! /usr/bin/env python

from functools import cmp_to_key
import sys
from ast import literal_eval

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        else:
            return 1 if left<right else -1

    if isinstance(left, list) and isinstance(right, list):
        if left == [] and right == []:
            return 0
        elif not left:
            return 1
        elif not right:
            return -1
        else:
            head_l, *tail_l = left
            head_r, *tail_r = right

            result = compare(head_l, head_r)
            if result == 0:
                return compare(tail_l, tail_r)
            else:
                return result
    else:
        if isinstance(left, int):
            return compare([left], right)
        else:
            return compare(left, [right])


pair = 1
ordered_pairs = []
for i in range(0, len(lines), 3):
    left = literal_eval(lines[i])
    right = literal_eval(lines[i+1])

    if compare(left, right) == 1:
        ordered_pairs.append(pair)
    pair += 1

print("Part 1:", sum(ordered_pairs))

divider_packets = [[[2]], [[6]]]
all_packets = list(literal_eval(l) for l in lines if l) + divider_packets
all_packets.sort(key=cmp_to_key(compare), reverse=True)
print("Part 2:", (all_packets.index(divider_packets[0])+1)*(all_packets.index(divider_packets[1])+1))
