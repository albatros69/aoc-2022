#! /usr/bin/env python

from dataclasses import dataclass
from functools import cache
from heapq import heappop, heappush
from itertools import product
import sys
import re
from time import perf_counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

@dataclass
class Valve():
    name: str
    flow_rate: int
    successors: list

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
re_line = re.compile(r"Valve (?P<name>[A-Z]{2}) has flow rate=(?P<flow_rate>[0-9]+); tunnels? leads? to valves? (?P<successors>.+)")
valves = {}
for l in lines:
    tmp = re_line.match(l)
    valves[tmp.group('name')] = Valve(
        tmp.group('name'), int(tmp.group('flow_rate')), tmp.group('successors').split(', '))

good_valves = set(v.name for v in valves.values() if v.flow_rate>0)
nb_good_valves = len(good_valves)


@cache
def explore_part1(current_valve, minutes, opened):
    if minutes <= 1 or len(opened) >= nb_good_valves:
        return 0

    result = 0
    V: Valve = valves[current_valve]

    result = max(result,
        *(explore_part1(v, minutes-1, opened) for v in V.successors))

    if V.flow_rate > 0 and V.name not in opened:
        result = max(result,
            explore_part1(V.name, minutes-1, opened|frozenset([V.name])) + V.flow_rate*(minutes-1)
        )

    return result

start = perf_counter()
print("Part 1:", explore_part1('AA', 30, frozenset()), "Execution time:", f'{perf_counter()-start:.3f}s')

@cache
def cost_move(start, dest, already_seen):
    if start == dest:
        return 0
    if start in already_seen:
        return sys.maxsize

    return 1 + min(cost_move(v, dest, already_seen|set((start, ))) for v in valves[start].successors)

start = perf_counter()
for (u,v) in product(set(('AA',))|good_valves, good_valves):
    # to populate the cache
    if u != v:
        cost_move(u,v, frozenset())
print("Populating cache:", f'{perf_counter()-start:.3f}s', flush=True)

@cache
def explore_part2_bad(current_valve_h, current_valve_e, minutes, opened):
    if minutes <= 1 or len(opened) >= nb_good_valves:
        return 0

    result = 0
    V_h: Valve = valves[current_valve_h]
    V_e: Valve = valves[current_valve_e]

    result = max(result,
        *(explore_part2_bad(u, v, minutes-1, opened) for (u,v) in product(V_h.successors, V_e.successors))
    )

    if V_h.name != V_e.name and \
        V_h.flow_rate > 0 and V_h.name not in opened and \
        V_e.flow_rate > 0 and V_e.name not in opened:
        new_opened = opened|frozenset([V_h.name, V_e.name])
        new_flow_rate = V_h.flow_rate*(minutes-1) + V_e.flow_rate*(minutes-1)

        result = max(result,
            explore_part2_bad(V_h.name, V_e.name, minutes-1, new_opened) + new_flow_rate
        )

    elif V_h.flow_rate > 0 and V_h.name not in opened:
        new_opened = opened|frozenset([V_h.name])
        new_flow_rate = V_h.flow_rate*(minutes-1)
        result = max(result,
            *(explore_part2_bad(V_h.name, v, minutes-1, new_opened) + new_flow_rate for v in V_e.successors)
        )

    elif V_e.flow_rate > 0 and V_e.name not in opened:
        new_opened = opened|frozenset([V_e.name])
        new_flow_rate = V_e.flow_rate*(minutes-1)
        result = max(result,
            *(explore_part2_bad(u, V_e.name, minutes-1, new_opened) + new_flow_rate for u in V_h.successors)
        )

    return result


@cache
def explore_part2_better(curr_h, min_h, curr_e, min_e, opened):
    if (min_h <= 1 and min_e <=1) or len(opened) >= nb_good_valves:
        return 0

    result = 0
    V_h: Valve = valves[curr_h]
    V_e: Valve = valves[curr_e]

    new_opened = opened
    if V_h.flow_rate > 0 and curr_h not in new_opened and min_h > 1:
        new_opened |= frozenset([curr_h])
        new_flow_rate = V_h.flow_rate*(min_h-1)
        result = max(result,
            explore_part2_better(curr_h, min_h-1, curr_e, min_e, new_opened) + new_flow_rate
        )

    if V_e.flow_rate > 0 and curr_e not in new_opened and min_e > 1:
        new_opened |= frozenset([curr_e])
        new_flow_rate = V_e.flow_rate*(min_e-1)
        result = max(result,
            explore_part2_better(curr_h, min_h, curr_e, min_e-1, new_opened) + new_flow_rate
        )

    possible_valves = good_valves - new_opened

    for (u, v) in product(possible_valves, repeat=2):
        if u == v:
            continue
        cost_u = cost_move(curr_h, u, frozenset())
        cost_v = cost_move(curr_e, v, frozenset())
        if cost_u > min_h or cost_v > min_e:
            continue

        result = max(result, explore_part2_better(u, min_h-cost_u, v, min_e-cost_v, new_opened))

    return result

# start = perf_counter()
# print("Part 2:", explore_part2_bad('AA', 'AA', 26, frozenset()), "Execution time:", f'{perf_counter()-start:.3f}s')
# start = perf_counter()
# print("Part 2:", explore_part2_better('AA', 26, 'AA', 26, frozenset()), "Execution time:", f'{perf_counter()-start:.3f}s')

queue = [ (0, 26, 26, 'AA', 'AA', frozenset()) ]
max_flow_rate = 0
already_seen = {}
start = perf_counter()
while queue:
    (curr_flow, min_h, min_e, curr_h, curr_e, opened) = heappop(queue)

    max_flow_rate = max(max_flow_rate, -curr_flow)
    if (min_h <= 1 and min_e <=1) or len(opened) >= nb_good_valves:
        continue

    if opened in already_seen and already_seen[opened] > -curr_flow:
        continue

    if -curr_flow + (max(min_e, min_h)-1)*sum(valves[v].flow_rate for v in (good_valves-opened)) < max_flow_rate:
        # this can't be a maximum already, even if you open the remaining valves all at once!
        continue

    already_seen[opened] = -curr_flow

    V_h: Valve = valves[curr_h]
    V_e: Valve = valves[curr_e]
    new_opened = opened
    if V_h.flow_rate > 0 and curr_h not in new_opened and min_h > 1:
        new_opened |= frozenset([curr_h])
        new_flow_rate = V_h.flow_rate*(min_h-1)
        heappush(queue, (curr_flow-new_flow_rate, min_h-1, min_e, curr_h, curr_e, new_opened))

    if V_e.flow_rate > 0 and curr_e not in new_opened and min_e > 1:
        new_opened |= frozenset([curr_e])
        new_flow_rate = V_e.flow_rate*(min_e-1)
        heappush(queue, (curr_flow-new_flow_rate, min_h, min_e-1, curr_h, curr_e, new_opened))

    possible_valves = good_valves - new_opened
    for (u, v) in product(possible_valves, repeat=2):
        if u == v:
            continue
        cost_u = cost_move(curr_h, u, frozenset())
        cost_v = cost_move(curr_e, v, frozenset())
        if cost_u > min_h or cost_v > min_e:
            continue

        if -curr_flow + (max(min_h-cost_u, min_e-cost_v)-1)*sum(valves[v].flow_rate for v in possible_valves) < max_flow_rate:
            # this can't be a maximum already, even if you open all the remaining valves at the next step!
            continue

        if new_opened in already_seen and already_seen[new_opened] > -curr_flow:
            continue

        heappush(queue, (curr_flow, min_h-cost_u, min_e-cost_v, u, v, new_opened))

print("Part 2:", max_flow_rate, "Execution time:", f'{perf_counter()-start:.3f}s')
