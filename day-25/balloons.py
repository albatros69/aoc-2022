#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

snafu_digits = { '2': 2, '1': 1, '0': 0, '-': -1, '=': -2 }
digits_snafu = { v: k for k,v in snafu_digits.items() }

def decimal2snafu(d: int):
    if d in digits_snafu:
        return digits_snafu[d]

    reminder = (d+2)%5 - 2
    return decimal2snafu((d-reminder)//5) + digits_snafu[reminder]

def snafu2decimal(s: str):
    if s in snafu_digits:
        return snafu_digits[s]

    return 5*snafu2decimal(s[:-1]) + snafu_digits[s[-1]]

# test1
# for l in lines:
#     print(f"{l:>10}", f"{decimal2snafu(int(l)):>13}")

# test2
# for l in lines:
#     print(f"{l:>10}", f"{snafu2decimal(l):>13}")

print("Part 1:", decimal2snafu(sum(snafu2decimal(l) for l in lines)))