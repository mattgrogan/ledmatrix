import os
import time

import randomcolor
from PIL import Image, ImageChops, ImageDraw, ImageFont

FONTFILE = os.path.join(os.path.dirname(__file__), "../../fonts/RPGSystem.ttf")
FONTSIZE = 16

SMALLFONT = os.path.join(os.path.dirname(
    __file__), "../../fonts/small_pixel.ttf")
SMALLFONTSIZE = 8


class Weather_Clock(object):

  def __init__(self, width, height):

    self.width = width
    self.height = height

    self.font = ImageFont.truetype(FONTFILE, FONTSIZE)
    self.small_font = ImageFont.truetype(SMALLFONT, SMALLFONTSIZE)

    self.time_color = None
    self.date_color = None
    self.old_time = None

    self.is_finished = False

  def randomize_colors(self, new_time=None, force=False):
    """ Pick some random colors """

    if new_time != self.old_time or force:

      rand_color = randomcolor.RandomColor()

      self.time_color = rand_color.generate()[0]
      self.date_color = rand_color.generate()[0]

      self.old_time = new_time

  def handle_input(self, command):

    if command == "ENTER":
      self.randomize_colors(force=True)

  def draw_frame(self):
    """ Draw the time on the screen """

    image = Image.new("RGB", (self.width, self.height))
    draw = ImageDraw.Draw(image)

    time_str = time.strftime("%I:%M", time.localtime()).lstrip("0")
    self.randomize_colors(time_str)

    w, h = self.small_font.getsize(time_str)
    xloc = (self.width - w) / 2

    draw.text((xloc, 2), time_str, font=self.small_font, fill=self.time_color)

    day_str = "WEATHER"
    draw.text((1, 12), day_str, font=self.small_font, fill=self.date_color)

    return image, 1000
