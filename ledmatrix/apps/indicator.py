
from PIL import Image, ImageDraw, ImageFont

from info.data import NOAA_Current_Observation
from components import Text, Icon

class Indicator_Image(object):
  """
  This object is responsible for composing an image given a list of
  components. As the image is animated, it will delegate the scrolling
  to each component.
  """

  def __init__(self, device):
    """
    The device is needed for its dimensions. The items will be cropped to
    fit within the screen.
    """

    self.device = device
    self._items = []

  def add_item(self, item, xy):
    """
    Store the item and its location as a tuple
    """

    self._items.append((item, xy))

  def build_image(self):
    """
    Build an image and paste each item into its appropriate location
    """

    # Create the blank image for this frame
    self.image = Image.new(self.device.mode, self.device.size)

    for item, xy in self._items:
      im = item.crop(self.device.size)
      im.load() # Force the crop
      self.image.paste(im, xy)

  def next(self):
    """
    Call move_left on each item in order to scroll the image. If all items
    are finished, then raise a StopIteration.
    """

    is_finished = True

    for item, xy in self._items:
      item.move_left()
      if not item.is_finished:
        is_finished = False # If any item is not finished, we're not finished

    if is_finished:
      raise StopIteration

  def reset(self):
    """
    Reset the positions of each child item.
    """

    for item, xy in self._items:
      item.reset()

SCROLL_IN = 0
PAUSE = 1
SCROLL_LEFT = 2
FINISHED = 3


class Indicator_Frame(object):

  def __init__(self, device, text):

    self.indicator_frame = Indicator_Image(device) #, "sunny", text)
    sunny = Icon.Icon("sunny")
    self.indicator_frame.add_item(sunny, (0,0))
    self.indicator_frame.add_item(Text(text), (0, sunny.size[1]))
    self.indicator_frame.build_image()

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
        self.indicator_frame.build_image()
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
