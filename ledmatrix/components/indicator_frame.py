from PIL import Image, ImageEnhance
from components import Icon, Text, NoScroll_Text, Indicator_Image


SCROLL_IN = 0
PAUSE = 1
SCROLL_LEFT = 2
FINISHED = 3
FADE_OUT = 4
FADE_IN = 5

MAX_FADE_IN = 0.60


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

    # How many cycles to scroll
    self.cycles = 1
    self.current_cycle = 1

    self.state = SCROLL_IN

  def add_item(self, item, xy):
    self.indicator_image.add_item(item, xy)

  @property
  def is_finished(self):

    return self.state == FINISHED

  def reset(self, scroll_in=False):
    if scroll_in:
      self.indicator_image.brightness = 1.0
      self.state = SCROLL_IN
    else:
      self.indicator_image.brightness = 0.0
      self.state = FADE_IN

  def draw_frame(self):
    """
    Draw the frame differently based on the current animation state.
    """

    if self.state == SCROLL_IN:
      # We're scrolling down from the top
      self.indicator_image.build_image()
      self.device.clear()
      try:
        self.indicator_image.move_down()

      except StopIteration:
        self.state = PAUSE

      self.device.image.paste(self.indicator_image.image, (0, 0))
      self.device.display()

    elif self.state == FADE_IN:

      self.indicator_image.brightness += 0.01

      if self.indicator_image.brightness <= MAX_FADE_IN:
        self.indicator_image.build_image()
        self.device.image = self.indicator_image.image
        self.device.display()
      else:
        self.indicator_image.reset()
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
      self.indicator_image.brightness -= 0.01

      if self.indicator_image.brightness >= 0:
        self.indicator_image.build_image()
        self.device.image = self.indicator_image.image
        self.device.display()
      else:
        self.indicator_image.reset()
        self.state = FINISHED

    return 50
