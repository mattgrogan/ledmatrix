import PIL.Image as Image
from components import Viewport_NoScroll_Mixin

class Icon(Viewport_NoScroll_Mixin):
  """ Create an icon image """

  @staticmethod
  def Icon(icon_name):

    if icon_name == "sunny":

      sunny = [0x020, 0x422, 0x204, 0x0F0,
               0x1F8, 0xDF8, 0x1FB, 0x1F8,
               0x0F0, 0x204, 0x442, 0x040]

      return Icon.Build(sunny)

  @staticmethod
  def Build(bitmap):

    im = Image.new("RGB", (12, 12))
    pix = im.load()

    for x in range(12):
      for y in range(12):
        row = bitmap[y]
        cell = row & (1 << (12 - x - 1))
        pix[x, y] = (255, 255, 0) if cell else (0, 0, 0)

    return Icon(im)

  def __init__(self, icon):

    self.image = icon
    self.reset()

  @property
  def size(self):

    return self.image.size
