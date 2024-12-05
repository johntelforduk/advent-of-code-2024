# Advent of code day 5, Print Queue.
# https://adventofcode.com/2024/day/5

from icecream import ic


def middle(l: list) -> int:
    return l[len(l) // 2]


assert middle([1]) == 1
assert middle([1,2,3]) == 2
assert middle([2,3,4,5,6]) == 4


with open('input.txt', 'r') as file:
    instructions = file.read()

rules_str, updates_str = instructions.split('\n\n')
# ic(rules_str, updates_str)

before_rules = {}
after_rules = {}

for rule in rules_str.split('\n'):
    b, a = [int(t) for t in rule.split('|')]

    if b not in before_rules:
        before_rules[b] = [a]
    else:
        before_rules[b].append(a)

    if a not in after_rules:
        after_rules[a] = [b]
    else:
        after_rules[a].append(b)

ic(before_rules, after_rules)

part1 = 0
for update_str in updates_str.split('\n'):
    update = [int(p) for p in update_str.split(',')]
    # ic(update, middle(update))

    before = []
    correct = True

    while len(update) != 0:
        this = update.pop(0)

        for b in before:
            if b in after_rules:
                if this in after_rules[b]:
                    correct = False

        for a in update:
            if a in before_rules:
                if this in before_rules[a]:
                    correct = False

        ic(before, this, update)


        before.append(this)

    if correct:
        part1 += middle(before)
    ic(before, correct)

ic(part1)
