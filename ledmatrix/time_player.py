import time

from PIL import Image, ImageChops, ImageDraw, ImageFont

import randomcolor

FONTFILE = "/home/pi/github/ledmatrix/fonts/RPGSystem.ttf"
FONTSIZE = 16

SMALLFONT = "/home/pi/github/ledmatrix/fonts/small_pixel.ttf"
SMALLFONTSIZE = 8


class Time_Player(object):
  """ Show the time and date """

  def __init__(self, matrix, width, height):
    """ Initialize the player """

    self.matrix = matrix
    self.width = width
    self.height = height

    self.font = ImageFont.truetype(FONTFILE, FONTSIZE)
    self.small_font = ImageFont.truetype(SMALLFONT, SMALLFONTSIZE)

    self.time_color = None
    self.date_color = None
    self.old_time = None

  def randomize_colors(self, new_time=None, force=False):
    """ Pick some random colors """

    if new_time != self.old_time or force:

      rand_color = randomcolor.RandomColor()

      self.time_color = rand_color.generate()[0]
      self.date_color = rand_color.generate()[0]

      self.old_time = new_time

  def move(self, step=None):
    """ Respond to the right and left remote buttons. Step value is ignored """

    self.randomize_colors(force=True)

  def draw_frame(self):
    """ Draw the time on the screen """

    image = Image.new("RGB", (self.width, self.height))
    draw = ImageDraw.Draw(image)

    time_str = time.strftime("%I:%M", time.localtime())
    self.randomize_colors(time_str)

    draw.text((1, -2), time_str, font=self.font, fill=self.time_color)

    day_str = time.strftime("%a", time.localtime())
    draw.text((1, 12), day_str, font=self.small_font, fill=self.date_color)

    date_str = time.strftime("%b %d", time.localtime())
    draw.text((1, 20), date_str, font=self.small_font, fill=self.date_color)

    self.matrix.SetImage(image.im.id)

    return 1
