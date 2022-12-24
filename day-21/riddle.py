#! /usr/bin/env python

from functools import cache
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

monkeys = {}
nb_monkeys = {}
for l in lines:
    m, r = l.split(': ')
    try:
        nb_monkeys[m] = int(r)
    except ValueError:
        monkeys[m] = r.split()


def ope(m1, op, m2):
    match op:
        case '+':
            return m1 + m2
        case '-':
            return m1 - m2
        case '*':
            return m1 * m2
        case '/':
            return m1 // m2

@cache
def solve(m):
    if m in nb_monkeys:
        return nb_monkeys[m]
    else:
        (m1, op, m2) = monkeys[m]
        return ope(solve(m1), op, solve(m2))

print("Part 1:", solve('root'))


def inv_ope(m, parent):
    (m1, op, m2) = monkeys[parent]
    match op:
        case '+':
            if m == m1:
                return (parent, '-', m2)
            else:
                return (parent, '-', m1)
        case '-':
            if m == m1:
                return (parent, '+', m2)
            else:
                return (m1, '-', parent)
        case '*':
            if m == m1:
                return (parent, '/', m2)
            else:
                return (parent, '/', m1)
        case '/':
            if m == m1:
                return (parent, '*', m2)
            else:
                return (m1, '/', parent)

parent_monkeys = {}
for m, t in monkeys.items():
    # Register which is the parent operation of a monkey
    parent_monkeys[t[0]] = m
    parent_monkeys[t[2]] = m
# To forget the number yelled in Part 1
del nb_monkeys['humn']

@cache
def rev_solve(m):
    if m in nb_monkeys:
        return nb_monkeys[m]
    else:
        parent = parent_monkeys[m]
        if parent == 'root':
            (m1, _, m2) = monkeys[parent]
            return solve(m2) if m1 == m else solve(m1)

        (m1, op, m2) = inv_ope(m, parent)
        return ope(
            rev_solve(m1) if m1==parent else solve(m1),
            op,
            rev_solve(m2) if m2==parent else solve(m2))

print("Part 2:", rev_solve('humn'))
