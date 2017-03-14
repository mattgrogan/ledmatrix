from PIL import Image, ImageEnhance
from components import Indicator_Image


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
    self.current_cycle = 1

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
