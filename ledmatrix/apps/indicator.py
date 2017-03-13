import os

from PIL import Image, ImageDraw, ImageFont

from device import Viewport
from drawable import Drawable

FONT_FOLDER = os.path.join(os.path.dirname(__file__), "../../fonts/%s.ttf")


class Frame(object):
  """
  Parent class for all frames
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


class Indicator_Frame(Frame):

  def __init__(self, device, text):

    self.device = device
    self.text = text

    # Determine the size of the text
    w, h = self.small_font.getsize(text)

    # The height is always the device height
    h = self.device.height

    # Pad width by device width for scrolling
    w += self.device.width

    # Create the blank image for this frame
    self.image = Image.new(device.mode, (w, h))

    # Add the text
    draw = ImageDraw.Draw(self.image)
    draw.text((0, 0), self.text, font=self.small_font)


class Indicator_Item(Drawable):

  def __init__(self, device):

    self.indicator_frame = Indicator_Frame(device, "Hello, world!")
    w, h = self.indicator_frame.image.size
    self.device = Viewport(device, w, h, self.indicator_frame.image)

  def draw_frame(self):

    scrolled = self.device.move_left()
    if not scrolled:
      self.device.set_position((0, 0))

    self.device.display()

    return 5
