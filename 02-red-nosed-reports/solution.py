# Advent of code day 2, Red-Nosed Reports.
# https://adventofcode.com/2024/day/2

from icecream import ic


def safe(report: list) -> bool:
    analysis = []
    prev = None
    for level in report:
        if prev is not None:
            diff = abs(level - prev)
            if diff > 3 or level == prev:
                return False
            elif level > prev:
                analysis.append('up')
            else:
                analysis.append('down')
        prev = level

    if 'up' in analysis and 'down' not in analysis or 'down' in analysis and 'up' not in analysis:
        return True
    return False


with open('input.txt', 'r') as file:
    reports = file.read()

list_of_reports = [[int(level) for level in line.split()] for line in reports.split('\n')]
ic(list_of_reports)

part1, part2 = 0, 0
for report in list_of_reports:
    if safe(report):
        part1 += 1
        part2 += 1
    else:
        found_safe = False
        for skip in range(len(report)):
            dampened = report.copy()
            dampened.pop(skip)
            if safe(dampened):
                found_safe = True
        if found_safe:
            part2 += 1

ic(part1, part2)
