# Advent of code day 11, Plutonian Pebbles.
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

    screenshot_name = 'screenshots/d11.png'
    pygame.image.save(screen, screenshot_name)
    pygame.display.flip()


with open('test2.txt', 'r') as file:
    garden_str = file.read()


garden = {}
my = 0
for row in garden_str.split('\n'):
    mx = 0
    for p in row:
        garden[(mx, my)] = p
        mx += 1
    my += 1

ic(garden)
ic(mx, my)

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

ic(v_fence, h_fence)
render(scale=50, mx=mx, my=my, garden=garden, v_fence=v_fence, h_fence=h_fence)
