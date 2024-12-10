# Advent of code day 10, Hoof It.
# https://adventofcode.com/2024/day/10

from icecream import ic
import pygame


def trailhead(topo: dict, x: int, y: int) -> int:
    height = topo[(x, y)]
    if height == 9:
        return 1

    count = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        xn, xy = x + dx, y + dy
        if (xn, xy) in topo:
            if topo[(xn, xy)] == height + 1:
                count += trailhead(topo, xn, xy)
    return count


def render(topo: dict, starts: dict, screen, scale: int):
    background_colour = (255, 255, 255)           # Black.
    screen.fill(background_colour)

    for x, y in topo:
        if (x, y) in starts:
            tile_col = (6 * starts[(x, y)], 0, 0)
        else:
            tile_col = (0, (1 + topo[(x, y)]) * 20, 0)
        pygame.draw.rect(screen, tile_col, pygame.Rect(x * scale, y * scale, scale, scale))

    screenshot_name = 'screenshots/d10p2.png'
    pygame.image.save(screen, screenshot_name)
    pygame.display.flip()




def trail_rating(topo: dict) -> (int, dict):
    total, progress = 0, 0
    starts = {}
    for x, y in topo:
        if y > progress:
            progress = y
            ic(progress)

        if topo[(x, y)] == 0:
            rating = trailhead(topo, x, y)
            ic(rating)
            starts[(x, y)] = rating
            total += rating
    return total, starts


with open('input.txt', 'r') as file:
    topo_str = file.read()

topo = {}
y = 0
for line in topo_str.split('\n'):
    x = 0
    for height_str in line:
        if height_str != '.':
            topo[(x, y)] = int(height_str)
        x += 1
    y += 1

scale = 14
screen_size = [scale * x, scale * y]  # [width, height]
pygame.init()                                               # Initialize the game engine.
screen = pygame.display.set_mode(screen_size)

tr, starts = trail_rating(topo)
ic(tr)
render(topo, starts, screen, scale)
