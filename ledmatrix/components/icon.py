from PIL import Image, ImageColor

from components import Viewport_NoScroll_Mixin


# TODO: Allow for different types of icons (scroll, noscroll, animated, etc.)


class Icon(Viewport_NoScroll_Mixin):
  """ Create an icon image """

  @staticmethod
  def Icon(icon_name, color="#FFFFFF"):

    return Icon.Build(BMP[icon_name], color)

  @staticmethod
  def Build(bitmap, color="#FFFFFF"):

    im = Image.new("RGB", (12, 12))
    pix = im.load()

    for x in range(12):
      for y in range(12):
        row = bitmap[y]
        cell = row & (1 << (12 - x - 1))
        pix[x, y] = ImageColor.getrgb(color) if cell else (0, 0, 0)

    return Icon(im)

  def __init__(self, icon):

    self.image = icon
    self.reset()

  @property
  def size(self):

    return self.image.size


BMP = {}
BMP["sunny"] = [0x020, 0x422, 0x204, 0x0F0,
                0x1F8, 0xDF8, 0x1FB, 0x1F8,
                0x0F0, 0x204, 0x442, 0x040]

BMP["cloud"] = [0x000, 0x000, 0x000, 0x018,
                0x1A4, 0x242, 0x402, 0x402,
                0x244, 0x1B8, 0x000, 0x000]

BMP["lightning"] = [0x008, 0x018, 0x030, 0x070,
                    0x0E0, 0x1FC, 0x3F8, 0x070,
                    0x0E0, 0x0C0, 0x180, 0x100]

BMP["house"] = [0x060, 0x0F0, 0x1F8, 0x3FC,
                0x7FE, 0xFFF, 0xFFF, 0x264,
                0x264, 0x3FC, 0x3FC, 0x3FC]
