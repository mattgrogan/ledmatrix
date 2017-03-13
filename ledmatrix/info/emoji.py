from PIL import Image

from device import Viewport
from drawable import Drawable


class Emoji(Drawable):

  def __init__(self, device):

    im = Image.new("RGB", device.size)
    x, y = im.size

    self.device = Viewport(device, x, y, im)

  def draw_frame(self):

    pix = self.device.image.load()

    sun = [0x020, 0x422, 0x204, 0x0F0,
           0x1F8, 0xDF8, 0x1FB, 0x1F8,
           0x0F0, 0x204, 0x442, 0x040]

    for x in range(12):
      for y in range(12):
        row = sun[y]
        cell = row & (1 << (12 - x - 1))
        pix[x, y] = (255, 0, 0) if cell else (0, 0, 0)

    self.device.display()

    return 100
