
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import time

from components import Icon, Text, NoScroll_Text
from info.data import NOAA_Current_Observation


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
      item.update()
      im = item.crop(self.device.size)
      im.load()  # Force the crop
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
        is_finished = False  # If any item is not finished, we're not finished

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
FADE_OUT = 4


class Indicator_Frame(object):
  """
  The frame object handles the animations. You must initialize and then add
  individual items to the frame. There is a scroll down animation
  at the beginning. Then a pause. And finally the items scroll to the left.
  """

  def __init__(self, device):
    """
    Create an image and set some options
    """

    self.device = device
    self.indicator_image = Indicator_Image(device)

    # How long to pause?
    self.frame_hold = 20
    self.current_hold = 0

    # Brightness
    self.brightness = 1.0

    # How many cycles to scroll
    self.cycles = 1
    self.current_cycle = 0

    # What's the bottom?
    self.y_loc = self.device.height - 1

    self.state = SCROLL_IN

  def add_item(self, item, xy):
    self.indicator_image.add_item(item, xy)

  @property
  def is_finished(self):

    return self.state == FINISHED

  def reset(self):
    self.state = SCROLL_IN

  def draw_frame(self):
    """
    Draw the frame differently based on the current animation state.
    """

    if self.state == SCROLL_IN:
      # We're scrolling down from the top
      self.indicator_image.build_image()
      self.device.clear()
      w, h = self.indicator_image.image.size
      self.indicator_image.image = self.indicator_image.image.crop(
          (0, self.y_loc, w - 1, h - 1))
      self.indicator_image.image.load()
      self.device.image.paste(self.indicator_image.image, (0, 0))

      self.device.display()

      self.y_loc -= 1

      # Check have we scrolled all the way?
      if self.y_loc < 0:
        self.y_loc = h
        self.state = PAUSE

    elif self.state == PAUSE:
      self.indicator_image.build_image()
      self.current_hold += 1
      self.device.image = self.indicator_image.image
      self.device.display()
      if self.current_hold > self.frame_hold:
        self.state = SCROLL_LEFT

    elif self.state == SCROLL_LEFT:
      try:
        self.indicator_image.next()
        self.indicator_image.build_image()
        self.device.image = self.indicator_image.image
        self.device.display()
      except StopIteration:
        self.current_hold = 0
        if self.current_cycle < self.cycles:
          self.current_cycle += 1
          self.indicator_image.reset()
          self.state = PAUSE
        else:
          self.state = FADE_OUT

    elif self.state == FADE_OUT:
      self.indicator_image.build_image()
      enhancer = ImageEnhance.Brightness(self.indicator_image.image)
      self.brightness -= 0.01

      if self.brightness >= 0:
        im = enhancer.enhance(self.brightness)
        self.device.image = im
        self.device.display()
      else:
        self.brightness = 1
        self.indicator_image.reset()
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
  Application to show information on the screen. This class handles the
  movement between different frames in the same application.
  """

  def __init__(self, device):
    """
    Initialize the item with the device (required for height and width)
    """

    self.device = device
    self._current_frame = 0
    self._frames = []

  def add_frame(self, frame):
    """
    Add a frame to this Application. The frames will be scrolled down and
    then to the left.
    """

    self._frames.append(frame)

  @property
  def current_frame(self):
    """
    Helper to point to the current frame
    """

    if len(self._frames) > self._current_frame:
      return self._frames[self._current_frame]

  def next(self):
    """
    Move to the next frame, or cycle back to the first frame.
    """
    self._current_frame += 1

    if self._current_frame >= len(self._frames):
      self._current_frame = 0

  def draw_frame(self):
    """
    Move to next frame if required. Draw the current frame.
    """

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
    sunny = Icon.Icon("sunny")
    temp_text = NoScroll_Text(self.temp)
    time_text = NoScroll_Text(self.time)
    long_text = Text(self.long_text)

    # Weather Frame
    w_frame = Indicator_Frame(device)
    w_frame.add_item(sunny, (1, 1))
    w_frame.add_item(temp_text, (sunny.size[0] + 2, 4))
    w_frame.add_item(long_text, (0, sunny.size[1] + 1))
    w_frame.add_item(time_text, (5, sunny.size[1] + long_text.size[1] + 2))

    self.add_frame(w_frame)
    self.add_frame(Indicator_Frame(device))  # Add a blank frame

  def long_text(self):
    text = self.cc["weather"]
    text += "   "
    text += self.date()
    text += "  Winds "
    text += self.cc["wind_string"]
    text += "  RH: "
    text += self.cc["relative_humidity"]
    text += "%  "
    text += self.cc["observation_time"]
    return text

  def weather(self):
    return self.cc["weather"]

  def temp(self):

    temp = self.cc["temp_f"]

    if temp is not None:
      temp = "%iF" % int(float(temp))  # Drop the decimal point
    else:
      temp = ""

    return temp

  def date(self):
    """ Return date in proper format """

    return time.strftime("%a %b %d", time.localtime())

  def time(self):
    """ Return the time in HH:MM format """

    return time.strftime("%I:%M", time.localtime()).lstrip("0")
