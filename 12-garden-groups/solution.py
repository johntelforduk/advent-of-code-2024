# Advent of code day 12, Garden Groups.
# https://adventofcode.com/2024/day/11

from icecream import ic
import pygame
import random


def render(scale: int, mx, my, garden, v_fence: set, h_fence: set):
    screen_size = [scale * (mx + 2), scale * (my + 2)]  # [width, height]
    pygame.init()  # Initialize the game engine.
    screen = pygame.display.set_mode(screen_size)
    background_colour = (255, 255, 255)           # Black.
    fence_colour = (0, 0, 0)
    screen.fill(background_colour)

    colours = {}
    for x, y in garden:
        plant = garden[(x, y)]
        if plant not in colours:
            colours[plant] = (2 * random.randint(0, 120),
                              2 * random.randint(0, 120),
                              2 * random.randint(0, 120))

        pygame.draw.rect(screen, colours[plant],
                         pygame.Rect((x + 1.15) * scale,
                                     (y + 1.15) * scale,
                                     scale * 0.7, scale * 0.7))

    for x, y in v_fence:
        pygame.draw.rect(screen, fence_colour,
                         pygame.Rect((0.85 + x) * scale, (1 + y) * scale, scale * 0.3, scale * 1.0))
    for x, y in h_fence:
        pygame.draw.rect(screen, fence_colour,
                         pygame.Rect((1 + x) * scale, (0.85 + y) * scale, scale * 1.0, scale * 0.3))

    screenshot_name = 'screenshots/d12.png'
    pygame.image.save(screen, screenshot_name)
    pygame.display.flip()


def search(garden: dict,
           v_fence: set,
           h_fence: set,
           x: int,
           y: int,
           p_found: set,
           v_found: set,
           h_found: set):
    if (x, y) in p_found:           # We've been here before.
        return
    p_found.add((x, y))             # Record that we've been here.

    if (x, y) in v_fence:
        v_found.add((x, y))
    else:
        search(garden, v_fence, h_fence, x - 1, y, p_found,v_found, h_found)

    if (x + 1, y) in v_fence:
        v_found.add((x + 1, y))
    else:
        search(garden, v_fence, h_fence, x + 1, y, p_found,v_found, h_found)

    if (x, y) in h_fence:
        h_found.add((x, y))
    else:
        search(garden, v_fence, h_fence, x, y - 1, p_found,v_found, h_found)

    if (x, y + 1) in h_fence:
        h_found.add((x, y + 1))
    else:
        search(garden, v_fence, h_fence, x, y + 1, p_found,v_found, h_found)


def rem_if_present(s: set, k):
    if k in s:
        s.remove(k)


def corners(p_found: set) -> int:
    count = 0
    for x, y in p_found:
        this_count = 0

        for check in [{False: [(-1, 0), (0, -1)]},  # These are the internal corners.
                      {False: [(0, -1), (1, 0)]},
                      {False: [(1, 0), (0, 1)]},
                      {False: [(0, 1), (-1, 0)]},

                        # These are the external corners.
                      {False: [(-1, -1)], True: [(-1, 0), (0, -1)]},
                      {False: [(1, -1)], True: [(0, -1), (1, 0)]},
                      {False: [(1, 1)], True: [(1, 0), (0, 1)]},
                      {False: [(-1, 1)], True: [(-1, 0), (0, 1)]}
                      ]:

            corner = True
            for condition in check:
                # ic(x, y, condition, check[condition])
                for xd, yd in check[condition]:
                    if condition and (x + xd, y + yd) not in p_found:
                        corner = False
                    if not condition and (x + xd, y + yd) in p_found:
                        corner = False
            if corner:
                # ic(x, y, check)
                this_count += 1
        count += this_count
    return count


with open('input.txt', 'r') as file:
    garden_str = file.read()


garden = {}
my = 0
for row in garden_str.split('\n'):
    mx = 0
    for p in row:
        garden[(mx, my)] = p
        mx += 1
    my += 1

# Like a computer graphics edge detection algorithm...
v_fence, h_fence = set(), set()
for y in range(my):
    v_fence.add((0, y))
    v_fence.add((mx, y))

for x in range(mx):
    h_fence.add((x, 0))
    h_fence.add((x, my))

for x1, y1 in garden:
    x2 = x1 + 1
    if (x2, y1) in garden:
        if garden[(x1, y1)] != garden[(x2, y1)]:
            v_fence.add((x2, y1))

    y2 = y1 + 1
    if (x1, y2) in garden:
        if garden[(x1, y1)] != garden[(x1, y2)]:
            h_fence.add((x1, y2))

render(scale=10, mx=mx, my=my, garden=garden, v_fence=v_fence, h_fence=h_fence)
p_found_ever = set()

part1, part2 = 0, 0
for x, y in garden:
    if (x, y) not in p_found_ever:
        p_found, v_found, h_found = set(), set(), set()
        search(garden, v_fence, h_fence, x, y, p_found,v_found, h_found)
        p_found_ever.update(p_found)

        price1 = len(p_found) * (len(v_found) + len(h_found))
        price2 = len(p_found) * corners(p_found)

        part1 += price1
        part2 += price2

        ic(x, y, part1, part2)
