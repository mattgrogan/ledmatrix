import os

import PIL.ImageFont as ImageFont

FONT_FOLDER = os.path.join(os.path.dirname(__file__), "../../fonts/%s.ttf")


class Font_Mixin(object):
  """
  Mixin provides font functionality
  """

  @property
  def small_font(self):

    return self.get_font("visitor1", 10)

  @property
  def medium_font(self):

    return self.get_font("small_pixel", 8)

  @property
  def large_font(self):

    # M12 should be 32px
    return self.get_font("m12", 16)

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
