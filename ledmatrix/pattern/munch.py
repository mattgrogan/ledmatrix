from colour import Color
from PIL import Image, ImageColor
from canvas import canvas
from components import App


class Pattern_Munch(App):

  def __init__(self, device):

    self.device = device
    self.width = device.width
    self.height = device.height

    self.count = 0
    self.dir = 1
    self.flip = 0
    self.generation = 0

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

    self.maxc = 0

  def draw_frame(self):

    with canvas(self.device) as draw:

      for x in range(self.width):
        for y in range(self.height):
          if (x ^ y ^ self.flip) < self.count:
            color_index = (self.generation % len(self.colors)) - 1
            color_index = (((x ^ y) << 3) + self.generation) % len(self.colors)
            c = self.colors[color_index]
            c = int(c.red * 255), int(c.green * 255), int(c.blue * 255)
            draw.point((x, y), fill=c)
          else:
            draw.point((x, y), fill=(0, 0, 0))

      self.count += self.dir

      if self.count <= 0 or self.count >= self.width:
        self.dir = -self.dir

      if self.count <= 0:
        if self.flip == 0:
          self.flip = 31
        else:
          self.flip = 0

      self.generation += 1

    return 10
