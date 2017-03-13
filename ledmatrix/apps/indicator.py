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


class Viewport_Mixin(object):
  """
  Mixin to help move around the image
  """

  def reset(self):
    """ Reset the viewport """

    self._position = (0, 0)

  def set_position(self, xy):

    self._position = xy

  def move_left(self):

    x, y = self._position
    self.set_position((x + 1, y))

  def crop(self, wh):
    """ Crop at width and height """

    w, h = wh

    (left, top) = self._position
    right = left + w
    bottom = top + h

    im = self.image.crop(box=(left, top, right, bottom))
    im.load()  # Force the crop
    return im

  @property
  def is_finished(self):

    x, y = self._position
    return x >= self.image.size[0]


class Text(Text_Mixin, Viewport_Mixin):
  """ Write text to an image """

  def __init__(self, text):

    self.text = text
    w, h = self.small_font.getsize(text)

    # Create the blank image for this frame
    self.image = Image.new("RGB", (w, h))

    # Add the text
    draw = ImageDraw.Draw(self.image)
    draw.text((0, 0), self.text, font=self.small_font)

    self.reset()

  @property
  def size(self):

    return self.image.size


class Icon(object):
  """ Create an icon image """

  def __init__(self):

    sunny = [0x020, 0x422, 0x204, 0x0F0,
             0x1F8, 0xDF8, 0x1FB, 0x1F8,
             0x0F0, 0x204, 0x442, 0x040]

    self.image = Image.new("RGB", (12, 12))
    pix = self.image.load()

    for x in range(12):
      for y in range(12):
        row = sunny[y]
        cell = row & (1 << (12 - x - 1))
        pix[x, y] = (255, 0, 0) if cell else (0, 0, 0)

  @property
  def size(self):
    return self.image.size


class Indicator_Frame(Viewport_Mixin):

  def __init__(self, device, text):

    self.device = device
    self.text = text

    self.icon_img = Icon()
    self.text_img = Text("Hello world xxxxx !!!")

    self.image = Image.new(self.device.mode, device.size)

  def reset(self):
    self.text_img.reset()

  def build_image(self):

    # Determine the size of the text
    w, h = self.text_img.size

    # The height is always the device height
    h = self.device.height

    # Pad width by device width for scrolling
    w = self.device.width

    # Create the blank image for this frame
    self.image = Image.new(self.device.mode, (w, h))

    # Add the icon
    self.image.paste(self.icon_img.image, (0, 0))

    # Add the text

    im = self.text_img.crop(self.device.size)
    im.load()
    self.image.paste(im, (0, self.icon_img.size[1]))

  @property
  def is_finished2(self):
    return self.text_img.is_finished

  def next(self):

    # Add the text
    self.text_img.move_left()

    self.build_image()

    if self.text_img.is_finished:
      raise StopIteration


class Indicator_Item(Drawable):

  def __init__(self, device):

    self.indicator_frame = Indicator_Frame(device, "Hello, world!")
    w, h = self.indicator_frame.image.size
    self.device = device  # Viewport(device, 32, 32)

    self.frame_hold = 20  # Hold for first # frames
    self.current_hold = 0

  def draw_frame(self):

    if self.current_hold >= self.frame_hold:
      try:
        self.indicator_frame.next()
      except StopIteration:
        self.indicator_frame.reset()
        self.current_hold = 0
    else:
      self.indicator_frame.build_image()

    # self.indicator_frame.image.load()
    self.device.image = self.indicator_frame.image
    self.device.display()

    #
    # if not scrolled:
    #   self.device.set_position((0, 0))
    #   self.current_hold = 0
    #
    # self.device.display()
    #
    self.current_hold += 1

    return 5
