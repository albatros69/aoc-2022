#! /usr/bin/env python

from functools import reduce
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Monkey():
    items: list
    operation: str
    divisor: int
    next_monkeys: dict
    activity: int

    def __init__(self, block):
        self.next_monkeys = {}
        self.activity = 0

        for l in block:
            field, value = l.strip().split(': ')
            if field.startswith("Starting"):
                self.items = [ int(a.strip()) for a in value.split(',') ]
            elif field.startswith("Operation"):
                self.operation = value.split('=')[1]
            elif field.startswith("Test"):
                self.divisor = int(value.split()[-1])
            elif field.startswith("If true"):
                self.next_monkeys[True] = int(value.split()[-1])
            elif field.startswith("If false"):
                self.next_monkeys[False] = int(value.split()[-1])

    def __str__(self):
        # return f"{self.items}, {self.operation}, {self.divider}, {self.next_monkeys}"
        return f"{self.items}"

    def __repr__(self) -> str:
        return str(self)

    def new_level(self, old):
        return eval(self.operation)

    def test(self, worry_level):
        return self.next_monkeys[worry_level%self.divisor == 0]

    def catch(self, item):
        self.items.append(item)


monkeys = {}
for i in range(0, len(lines), 7):
    if lines[i].startswith("Monkey"):
        nb = int(lines[i].split()[1][:-1])
        monkeys[nb] = Monkey(lines[i+1:i+6])

# for a,m in monkeys.items():
#     print(f"Monkey {a}: {m}")

for step in range(20):
    for m in monkeys.values():
        m.activity += len(m.items)
        while m.items:
            l = m.items.pop(0)
            new_l = m.new_level(l)//3
            next_monkey = m.test(new_l)
            monkeys[next_monkey].catch(new_l)

# print("Round", step+1)
# for a,m in activity.items():
#     print(f"Monkey {a}: {m}")

tmp = sorted(m.activity for m in monkeys.values())
print("Part 1:", tmp[-1]*tmp[-2])

monkeys = {}
for i in range(0, len(lines), 7):
    if lines[i].startswith("Monkey"):
        nb = int(lines[i].split()[1][:-1])
        monkeys[nb] = Monkey(lines[i+1:i+6])

modulus = reduce(lambda x,y: x*y, (m.divisor for m in monkeys.values()))
for step in range(10000):
    for m in monkeys.values():
        m.activity += len(m.items)
        while m.items:
            l = m.items.pop(0)
            new_l = m.new_level(l)%modulus
            next_monkey = m.test(new_l)
            monkeys[next_monkey].catch(new_l)

# print("Round", step+1)
# for a,m in activity.items():
#     print(f"Monkey {a}: {m}")

tmp = sorted(m.activity for m in monkeys.values())
print("Part 2:", tmp[-1]*tmp[-2])
