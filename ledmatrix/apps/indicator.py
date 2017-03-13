import os

from PIL import Image, ImageDraw, ImageFont

from device import Viewport
from drawable import Drawable

FONT_FOLDER = os.path.join(os.path.dirname(__file__), "../../fonts/%s.ttf")


class Text_Mixin(object):
  """
  Mixin provides font functionality
  """
  @property
  def small_font(self):
    """
    Return a small font for drawing
    """

    return self.get_font("small_pixel", 8)

  def get_font(self, name, size):
    """
    Obtain a font from the font folder

    :param string name:
      The name of the truetype font. Do not include the file extension.

    :param int size:
      Size of the font in points.
    """

    font_file = FONT_FOLDER % name
    font = ImageFont.truetype(font_file, size)

    return font


class Text(Text_Mixin):
  """ Write text to an image """

  def __init__(self, text):

    self.text = text
    w, h = self.small_font.getsize(text)

    # Create the blank image for this frame
    self.image = Image.new("RGB", (w, h))

    # Add the text
    draw = ImageDraw.Draw(self.image)
    draw.text((0, 0), self.text, font=self.small_font)

  @property
  def size(self):

    return self.image.size


class Icon(object):
  """ Create an icon image """

  def __init__(self):

    sunny = [0x020, 0x422, 0x204, 0x0F0,
             0x1F8, 0xDF8, 0x1FB, 0x1F8,
             0x0F0, 0x204, 0x442, 0x040]

    self.image = Image.new("1", (12, 12))
    pix = self.image.load()

    for x in range(12):
      for y in range(12):
        row = sunny[y]
        cell = row & (1 << (12 - x - 1))
        pix[x, y] = cell

  @property
  def size(self):
    return self.image.size


class Indicator_Frame(object):

  def __init__(self, device, text):

    self.device = device
    self.text = text

    icon_img = Icon()
    text_img = Text("Hello world 2 !!!")

    # Determine the size of the text
    w, h = text_img.size

    # The height is always the device height
    h = self.device.height

    # Pad width by device width for scrolling
    w += self.device.width

    # Create the blank image for this frame
    self.image = Image.new(device.mode, (w, h))

    # Add the text
    self.image.paste(icon_img.image, (0, 0))
    self.image.paste(text_img.image, (0, icon_img.size[1]))


class Indicator_Item(Drawable):

  def __init__(self, device):

    self.indicator_frame = Indicator_Frame(device, "Hello, world!")
    w, h = self.indicator_frame.image.size
    self.device = Viewport(device, w, h, self.indicator_frame.image)

    self.frame_hold = 20  # Hold for first 10 frames
    self.current_hold = 0

  def draw_frame(self):

    if self.current_hold >= self.frame_hold:
      scrolled = self.device.move_left()
    else:
      scrolled = True

    if not scrolled:
      self.device.set_position((0, 0))
      self.current_hold = 0

    self.device.display()

    self.current_hold += 1

    return 5
