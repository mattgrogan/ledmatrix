
from PIL import Image, ImageDraw, ImageFont

from info.data import NOAA_Current_Observation
from components import Text


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


class Indicator_Image(object):

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
FINISHED = 3


class Indicator_Frame(object):

  def __init__(self, device, text):

    self.indicator_frame = Indicator_Image(device, text)
    w, h = self.indicator_frame.image.size
    self.device = device

    self.frame_hold = 20  # Hold for first # frames
    self.current_hold = 0

    self.y_loc = h - 1

    self.state = SCROLL_IN

  def handle_input(self, command):

    pass

  @property
  def is_finished(self):

    return self.state == FINISHED

  def reset(self):
    self.state = SCROLL_IN

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
        # self.indicator_frame.image.load()
        self.device.image = self.indicator_frame.image
        self.device.display()
      except StopIteration:
        self.indicator_frame.reset()
        self.current_hold = 0
        self.state = FINISHED

    return 50


class App(object):
  """
  Application to show animations or information on the screen
  """

  def handle_input(self, command):

    pass

  def draw_frame(self):

    raise NotImplementedError


class Indicator_App(App):
  """
  Application to show information on the screen.
  """

  def __init__(self, device):

    self.device = device
    self._current_frame = 0
    self._frames = []

  def add_frame(self, frame):

    self._frames.append(frame)

  @property
  def current_frame(self):

    if len(self._frames) > self._current_frame:
      return self._frames[self._current_frame]

  def next(self):
    self._current_frame += 1

    if self._current_frame >= len(self._frames):
      self._current_frame = 0

  def draw_frame(self):

    # TODO: Check if current frame is finished
    if self.current_frame.is_finished:
      self.next()
      self.current_frame.reset()

    return self.current_frame.draw_frame()


class Weather_App(Indicator_App):

  def __init__(self, device, station):

    super(Weather_App, self).__init__(device)

    self.device = device
    self.station = station
    self.cc = NOAA_Current_Observation(station)

    # Build frames
    temp_frame = Indicator_Frame(device, self.cc["temperature_string"])
    weather_frame = Indicator_Frame(device, self.cc["weather"])

    self.add_frame(temp_frame)
    self.add_frame(weather_frame)
