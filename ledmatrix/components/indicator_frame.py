from PIL import Image, ImageEnhance
from components import Icon, Text, NoScroll_Text, Indicator_Image, Indicator_Image_Control, Image_Pause_Control, Image_ScrollDown_Control, Image_FadeIn_Control, Image_FadeOut_Control, Image_ScrollLeft_Control


SCROLL_IN = 0
PAUSE = 1
SCROLL_LEFT = 2
FINISHED = 3
FADE_OUT = 4
FADE_IN = 5

MAX_FADE_IN = 0.70
PAUSE_FRAMES = 10


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
    ic = Indicator_Image_Control()
    self.indicator_image = Indicator_Image(device, ic)

    self.reset(scroll_in=True)

  def add_item(self, item, xy):
    self.indicator_image.add_item(item, xy)

  @property
  def is_finished(self):

    return self.state == FINISHED

  def reset(self, scroll_in=False):
    if scroll_in:
      self.indicator_image.brightness = 1.0
      self.state = SCROLL_IN
      self.device.clear()
      self.indicator_image.image_control = Image_ScrollDown_Control()
    else:
      self.indicator_image.brightness = 0.0
      self.indicator_image.image_control = Image_FadeIn_Control(0.70)
      self.state = FADE_IN

  def handle_input(self, command):
    pass

  def draw_frame(self):
    """
    Draw the frame differently based on the current animation state.
    """

    if self.state == FINISHED:
      self.reset()

    try:
      self.indicator_image.display()
    except StopIteration:

      if self.state == SCROLL_IN:
        self.indicator_image.image_control = Image_Pause_Control(PAUSE_FRAMES)
        self.state = PAUSE

      elif self.state == FADE_IN:
        self.state = PAUSE
        self.indicator_image.image_control = Image_Pause_Control(PAUSE_FRAMES)

      elif self.state == PAUSE:
        self.indicator_image.image_control = Image_ScrollLeft_Control()
        self.state = SCROLL_LEFT

      elif self.state == SCROLL_LEFT:
        self.state = FADE_OUT
        self.indicator_image.image_control = Image_FadeOut_Control()

      elif self.state == FADE_OUT:
        self.indicator_image.reset()
        self.indicator_image.image_control = Indicator_Image_Control()
        self.state = FINISHED

    return 50
