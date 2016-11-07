# Source:https://github.com/FastLED/FastLED/blob/master/examples/Fire2012WithPalette/Fire2012WithPalette.ino
from __future__ import division

import math
import random

from colour import Color
#import randomcolor
from PIL import Image, ImageChops, ImageDraw, ImageFont


def hex_to_rgb(value):
  value = value.lstrip('#')
  lv = len(value)
  return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class Pattern_Fire(object):
  """ Create a fire animation """

  def __init__(self, width, height):

    self.width = width
    self.height = height

    self.heat = [[0 for x in range(width)] for y in range(height)]

    # COOLING: How much does the air cool as it rises?
    # Less cooling = taller flames.  More cooling = shorter flames.
    # Default 55, suggested range 20-100
    self.cooling = 30

    # SPARKING: What chance (out of 255) is there that a new spark will be lit?
    # Higher chance = more roaring fire.  Lower chance = more flickery fire.
    # Default 120, suggested range 50-200.
    self.sparking = 80

    black = Color("black")
    red = Color("red")
    yellow = Color("yellow")
    white = Color("white")

    self.colors = []
    self.colors += list(black.range_to(red, 126))
    self.colors += list(red.range_to(yellow, 100))
    self.colors += list(yellow.range_to(white, 30))

    self.image = None

  def move(self, step=1):

    self.image = Image.new("RGB", (self.width, self.height))
    pix = self.image.load()

    for x in range(self.width):

      # Step 1: cool down every cell a little
      for y in range(self.height):
        cooling_factor = random.randint(
            0, int(((self.cooling * 32) / self.height)))
        self.heat[x][y] = max(self.heat[x][y] - cooling_factor, 0)

      # Step 2: Heat from each cell drifts up and diffuses a little
      for y in range(self.height):
        y1 = min(y + 1, self.height - 1)
        y2 = min(y + 2, self.height - 1)
        self.heat[x][y] = (self.heat[x][y1] + self.heat[x]
                           [y2] + self.heat[x][y2]) / 3

      # Step 3: Randomly ignite sparks of heat
      if random.randrange(0, 255) < self.sparking:
        y0 = self.height - 1
        self.heat[x][y0] = min(
            (self.heat[x][y0] + random.randrange(160, 255)), 255)

      # Step 4: Map to the colors
      for y in range(self.height):
        color_index = int(self.heat[x][y])  # int(math.ceil(self.heat[x][y]))
        c = self.colors[color_index]
        pix[x, y] = (int(c.red * 255), int(c.green * 255), int(c.blue * 255))

  def draw_frame(self):

    self.move()

    return self.image, 25