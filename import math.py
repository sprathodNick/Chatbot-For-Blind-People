import math
import random
import sys

from PIL import Image, ImageDraw

try:
    from scipy.spatial import cKDTree as KDTree
    import numpy as np
    IMPORTED_SCIPY = True
    
except ImportError:
    IMPORTED_SCIPY = False

BACKGROUND = (255, 255, 255)
TOTAL_CIRCLES = 1500

color = lambda c: ((c >> 16) & 255, (c >> 8) & 255, c & 255)

COLORS_ON = [
    color(0xF9BB82), color(0xEBA170), color(0xFCCD84)
]
COLORS_OFF = [
    color(0x9CA594), color(0xACB4A5), color(0xBBB964),
    color(0xD7DAAA), color(0xE5D57D), color(0xD1D6AF)
]


def generate_circle(image_width, image_height, min_diameter, max_diameter):
    radius = random.triangular(min_diameter, max_diameter,
                               max_diameter * 0.8 + min_diameter * 0.2) / 2

    angle = random.uniform(0, math.pi * 2)
    distance_from_center = random.uniform(0, image_width * 0.48 - radius)
    x = image_width  * 0.5 + math.cos(angle) * distance_from_center
    y = image_height * 0.5 + math.sin(angle) * distance_from_center

    return x, y, radius
    
    def overlaps_motive(image, circle):
    x, y, r = circle
    points_x = [x, x, x, x-r, x+r, x-r*0.93, x-r*0.93, x+r*0.93, x+r*0.93]
    points_y = [y, y-r, y+r, y, y, y+r*0.93, y-r*0.93, y+r*0.93, y-r*0.93]

    for xy in zip(points_x, points_y):
        if image.getpixel(xy)[:3] != BACKGROUND:
            return True

    return False
    def circle_intersection(circle1, circle2):
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    return (x2 - x1)*2 + (y2 - y1)2 < (r2 + r1)*2


def circle_draw(draw_image, image, circle):
    fill_colors = COLORS_ON if overlaps_motive(image, circle) else COLORS_OFF
    fill_color = random.choice(fill_colors)

    x, y, r = circle
    draw_image.ellipse((x - r, y - r, x + r, y + r),
                       fill=fill_color,
                       outline=fill_color)