import os

from PIL import ImageFont

FONT_FOLDER = os.path.join(os.path.dirname(__file__), "../fonts/%s.otf")


class Drawable(object):
  """
  Parent class for drawing onto the matrix.
  """

  @property
  def small_font(self):
    """
    Return a small font for use.
    """

    return self.get_font("Unibody8Pro-Regular", 8)

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

  def handle_input(self, command):

    pass

  def draw_frame(self):

    raise NotImplementedError
