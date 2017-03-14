
from PIL import Image, ImageDraw, ImageFont

from components import Font_Mixin, Viewport_Mixin


class Text(Font_Mixin, Viewport_Mixin):
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


class Indicator_Frame(object):

  def __init__(self, device, text):

    self.device = device
    self.text = text

    self.icon_img = Icon()
    self.text_img = Text(text)

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

  def next(self):

    # Add the text
    self.text_img.move_left()

    self.build_image()

    if self.text_img.is_finished:
      raise StopIteration


SCROLL_IN = 0
PAUSE = 1
SCROLL_LEFT = 2


class Indicator_Item(object):

  def __init__(self, device):

    self.indicator_frame = Indicator_Frame(device, "Hello, world!")
    w, h = self.indicator_frame.image.size
    self.device = device

    self.frame_hold = 20  # Hold for first # frames
    self.current_hold = 0

    self.y_loc = h - 1

    self.state = SCROLL_IN

  def handle_input(self, command):

    pass

  def draw_frame(self):

    if self.state == SCROLL_IN:
      self.indicator_frame.build_image()
      self.device.clear()
      w, h = self.indicator_frame.image.size
      self.indicator_frame.image = self.indicator_frame.image.crop(
          (0, self.y_loc, w - 1, h - 1))
      self.indicator_frame.image.load()
      self.device.image.paste(self.indicator_frame.image, (0, 0))

      self.device.display()

      self.y_loc -= 1

      if self.y_loc < 0:
        self.y_loc = h
        self.state = PAUSE

    elif self.state == PAUSE:
      self.indicator_frame.build_image()
      self.current_hold += 1
      self.device.image = self.indicator_frame.image
      self.device.display()
      if self.current_hold > self.frame_hold:
        self.state = SCROLL_LEFT

    elif self.state == SCROLL_LEFT:
      try:
        self.indicator_frame.next()
      except StopIteration:
        self.indicator_frame.reset()
        self.current_hold = 0
        self.state = SCROLL_IN

      # self.indicator_frame.image.load()
      self.device.image = self.indicator_frame.image
      self.device.display()

    return 15
