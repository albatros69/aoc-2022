#! /usr/bin/env python

import sys
from dataclasses import dataclass
from collections import deque
from multiprocessing import Pool

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


@dataclass(frozen=True)
class Robot():
    product: str
    costs: tuple

def update_dict(d, u):
    for k,v in u:
        d[k] += v
    return d.copy()

blueprints = dict()
for l in lines:
    bp, robots = l.split(':', maxsplit=1)
    bp = int(bp.split()[1])

    blueprints[bp] = []
    for r in robots.split('. '):
        _, p, _, _, c = r.split(maxsplit=4)
        tmp = {}
        for x in c.split(' and '):
            v,k = x.split()
            tmp[k.rstrip('.')] = -int(v)
        blueprints[bp].append(Robot(p, tuple(tmp.items())))

    blueprints[bp] = tuple(blueprints[bp])

def possible_factory_strategies(mat, rob, bp, time):
    maxi_m = { k: max(abs(dict(r.costs).get(k, 0)) for r in bp) for k in ('ore', 'clay', 'obsidian') }
    result = set(((mat, rob), ))

    tmp_m = dict(mat)
    for r in bp:
        if all(tmp_m[a]+v >= 0 for a,v in r.costs):
            new_rob = dict(rob)
            new_mat = dict(mat)
            new_rob[r.product] += 1
            update_dict(new_mat, r.costs)
            for k,v in maxi_m.items():
                # No need for more robots than we can consume
                new_rob[k] = min(new_rob[k], v)
                # No need to stockpile materials we will never have time to consume
                new_mat[k] = min(new_mat[k], v*time - new_rob[k]*(time-1))
            result.add((tuple(new_mat.items()), tuple(new_rob.items())))

    return result


def solve(start_time, bp):

    materials = (('ore', 0), ('clay', 0), ('obsidian', 0), ('geode', 0))
    robots = (('ore', 1), ('clay', 0), ('obsidian', 0), ('geode', 0))

    queue = deque([ (start_time, materials, robots) ])
    max_geodes = 0
    already_seen = set()
    maxi_m = { k: max(abs(dict(r.costs).get(k, 0)) for r in bp) for k in ('ore', 'clay', 'obsidian') }

    while queue:
        time, m, r = queue.popleft()

        nb_geodes = dict(m)['geode']
        r_geodes = dict(r)['geode']

        max_geodes = max(max_geodes, nb_geodes)
        if time == 0:
            continue
        if max_geodes > nb_geodes + r_geodes*time:
            continue
        if any(dict(r)[k] > maxi_m[k] for k in maxi_m):
            continue

        if (time, m, r) in already_seen:
            continue
        already_seen.add((time, m, r))

        for (new_m, new_r) in possible_factory_strategies(m, r, bp, time):
            tmp = dict(new_m)
            update_dict(tmp, r)
            new_state = (time-1, tuple(tmp.items()), new_r)
            if new_state not in already_seen:
                queue.append(new_state)

    return max_geodes


# result = 0
# for i,bp in blueprints.items():
#     tmp = solve(24, bp)
#     print("BP", i, "-> Geodes:", tmp)
#     result += i*tmp

def solve_p1(a):
    i, bp = a
    tmp = solve(24, bp)
    print("BP", i, "-> Geodes:", tmp)
    return i*tmp

with Pool() as p:
    result = sum(p.imap_unordered(solve_p1, blueprints.items()))

print("Part 1:", result)


# result = 1
# for i,bp in blueprints.items():
#     if i > 3:
#         continue
#     tmp = solve(32, bp)
#     print("BP", i, "-> Geodes:", tmp)
#     result *= tmp

def solve_p2(a):
    i, bp = a
    tmp = solve(32, bp)
    print("BP", i, "-> Geodes:", tmp)
    return tmp

result = 1
with Pool() as p:
    for t in p.imap_unordered(
        solve_p2,
        ((i,bp) for (i,bp) in blueprints.items() if i <= 3)):
        result *= t

print("Part 2:", result)

