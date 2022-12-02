#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n').split())

corresp = {
    "A": "R", "X": "R",
    "B": "P", "Y": "P",
    "C": "S", "Z": "S"
}
scores = dict(zip("RPS", (1,2,3)))
wins = (("R", "S"), ("S", "P"), ("P", "R"))

def round(a, b):
    if (a, b) in wins:
        return 0 + scores[b]
    elif (b, a) in wins:
        return 6 + scores[b]
    else:
        return 3 + scores[b]

total = 0
for (elve, me) in lines:
    total += round(corresp[elve], corresp[me])

print("Part 1:", total)

me_loses = dict(wins)
me_wins = dict(a[::-1] for a in wins)
def corresp_part2(elve, outcome):
    if outcome == "X":
        return me_loses[elve]
    elif outcome == "Y":
        return elve
    elif outcome == "Z":
        return me_wins[elve]

total = 0
for (elve, outcome) in lines:
    total += round(corresp[elve], corresp_part2(corresp[elve], outcome))

print("Part 1:", total)
