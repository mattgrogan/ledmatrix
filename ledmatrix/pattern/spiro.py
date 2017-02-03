from __future__ import division

import math

from colour import Color
from PIL import Image, ImageColor


def scale(val, src, dst):
  """
  Scale the given value from the scale of src to the scale of dst.
  """
  return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


class Pattern_Spiro(object):

  def __init__(self, width, height):

    self.width = width
    self.height = height

    self.matrix_center_x = Int(self.width / 2)
    self.matrix_center_y = Int(self.height / 2)

    self.theta1 = 0
    self.theta2 = 0
    self.hueoffset = 0

    self.radiusx = self.width / 4
    self.radiusy = self.height / 4
    self.minx = self.matrix_center_x - self.radiusx
    self.maxx = self.matrix_center_x + self.radiusx + 1
    self.miny = self.matrix_center_y + self.radiusy
    self.maxy = self.matrix_center_y + self.radiusy + 1

    self.spiro_count = 1
    self.spiro_offset = 256 / self.spiro_count
    self.spiro_increment = False

    self.handled_change = False

    blue = Color("blue")
    green = Color("green")
    yellow = Color("yellow")
    orange = Color("orange")
    red = Color("red")
    purple = Color("purple")

    self.colors = []
    self.colors += list(blue.range_to(green, 100))
    self.colors += list(green.range_to(purple, 100))
    self.colors += list(purple.range_to(blue, 100))

    self.image = Image.new("RGB", (self.width, self.height))
    self.pix = self.image.load()

  def draw_frame(self):

    change = False

    for i in range(self.spiro_count):
      sinx = theta + i * self.spiro_offset
      x = scale(math.sin(sinx, ()))
