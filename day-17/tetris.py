#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))
winds = lines[0]

def next_rock(h, c):
    m = c % 5
    h += 4
    if m == 0:
        return {2 + h * 1j, 3 + h * 1j, 4 + h * 1j, 5 + h * 1j}
    elif m == 1:
        return {3 + h * 1j, 2 + (h+1) * 1j, 3 + (h+1) * 1j, 4 + (h+1) * 1j, 3 + (h+2) * 1j}
    elif m == 2:
        return {2 + h * 1j, 3 + h * 1j, 4 + h * 1j, 4 + (h+1) * 1j, 4 + (h+2) * 1j}
    elif m == 3:
        return {2 + h * 1j, 2 + (h+1) * 1j, 2 + (h+2) * 1j, 2 + (h+3) * 1j}
    elif m == 4:
        return {2 + h * 1j, 3 + h * 1j, 2 + (h+1) * 1j, 3 + (h+1) * 1j}

def move_rock_right(rock):
    if any(x.real == 6 for x in rock):
        return rock
    return { x + 1 for x in rock }

def move_rock_left(rock):
    if any(x.real == 0 for x in rock):
        return rock
    return { x - 1 for x in rock }

def move_rock_down(rock):
    return { x - 1j for x in rock }


nb_rocks = 0
moves, height = 0, 0
chamber = { x+0j for x in range(7) }
cycles = dict()
max_rocks = 1000000000000
while nb_rocks < max_rocks:

    # Moving the next rock till it hits something
    new_rock = next_rock(height, nb_rocks)
    while True:
        tmp = move_rock_left(new_rock) if winds[moves]  == '<' else move_rock_right(new_rock)
        if not chamber & tmp:
            new_rock = tmp
        moves = (moves + 1) % len(winds)
        tmp = move_rock_down(new_rock)
        if chamber & tmp: # We hit something
            chamber.update(new_rock)
            height = max(height, *(int(z.imag) for z in new_rock))
            break
        else: # We continue
            new_rock = tmp

    nb_rocks += 1
    if nb_rocks == 2022:
        print("Part 1:", height)
    if nb_rocks > 2022 and (nb_rocks%5, moves) in cycles:
        h_c, rocks_c = cycles[nb_rocks%5, moves]
        delta_h = height - h_c
        delta_rocks = nb_rocks - rocks_c
        nb_cycles = (max_rocks - nb_rocks)//delta_rocks
        nb_rocks += delta_rocks*nb_cycles
        height_offset = delta_h*nb_cycles
        cycles.clear() # to reset the cycle detection

    cycles[nb_rocks%5, moves] = (height, nb_rocks)

print("Part 2:", height + height_offset)




