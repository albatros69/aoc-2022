#! /usr/bin/env python

from __future__ import annotations
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Node():
    type: str
    name: str
    size: int
    parent: Node
    subnodes: dict[Node]

    def __init__(self, type, name, size=0, parent=None) -> None:
        self.type = type
        self.name = name
        if type == 'f':
            self.size = size
        else:
            self.size = 0
        self.parent = parent
        self.subnodes = {}
        self._total_size = None

    def __str__(self) -> str:
        if self.type == 'f':
            return f'{self.name} (file, size={self.size})'
        elif self. type == 'd':
            return f'{self.name} (dir)'

    def read_ls(self, line):
        if line.startswith("dir"):
            _, name = line.split()
            self.subnodes[name] = Node('d', name, parent=self)
        else:
            size, name = line.split()
            self.subnodes[name] = Node('f', name, int(size), self)

    def print(self, indent='-'):
        print(indent, str(self))
        for d in self.subnodes.values():
            d.print('  ' + indent)

    def total_size(self):
        if self._total_size is None:
            self._total_size = self.size + sum(d.total_size() for d in self.subnodes.values())
        return self._total_size

    def find_small(self, limit=100000):
        result = [ self ] if self.total_size() <= limit else []
        for d in self.subnodes.values():
            if d.type == 'd':
                result.extend(d.find_small(limit))
        return result

    def find_big(self, limit=100000):
        result = [ self ] if self.total_size() >= limit else []
        for d in self.subnodes.values():
            if d.type == 'd':
                result.extend(d.find_big(limit))
        return result


root = Node('d', '/')
working_dir = root
in_ls = False
for l in lines:
    if l.startswith("$ cd"):
        in_ls = False
        args = l.split()[-1]
        if args == '/':
            working_dir = root
        elif args == '..':
            if working_dir.parent is not None:
                working_dir = working_dir.parent
        else:
            working_dir = working_dir.subnodes[args]
    elif l.startswith("$ ls"):
        in_ls = True
    elif in_ls:
        working_dir.read_ls(l)

# root.print()
print("Part 1:", sum(d.total_size() for d in root.find_small()))
free_space = 70000000 - root.total_size()
to_delete = min(root.find_big(30000000-free_space), key=lambda x: x.total_size())
print("Part 2:", to_delete.total_size())
