from __future__ import division

import math
import os
import time
from canvas import canvas

import randomcolor
from PIL import Image, ImageChops, ImageDraw, ImageFont

FONTFILE = os.path.join(os.path.dirname(__file__), "../../fonts/RPGSystem.ttf")
FONTSIZE = 16

SMALLFONT = os.path.join(os.path.dirname(
    __file__), "../../fonts/small_pixel.ttf")
SMALLFONTSIZE = 8


class Countdown(object):
  """ Show the time until NYE """

  def __init__(self, device):
    """ Initialize the player """

    self.device = device

    self.width = device.width
    self.height = device.height

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

    with canvas(self.device) as draw:

      nye = time.mktime(time.strptime("01 Jan 17", "%d %b %y"))
      now = time.mktime(time.localtime())
      countdown_secs = nye - now

      green = "#88fc95"
      red = "#f41f3c"
      yellow = "#fce40f"
      blue = "#709fea"

      color1 = blue
      color2 = green

      if countdown_secs > 0:

        # rand_color = randomcolor.RandomColor()

        hours = math.floor(countdown_secs / 60 / 60)
        mins = math.floor(countdown_secs / 60)
        secs = round(countdown_secs, 0)

        hour_str = "%i hrs" % hours
        min_str = "%i min" % mins
        sec_str = "%i" % secs

        # self.randomize_colors(min_str) # Change colors once per min

        draw.text((self.x(hour_str), 0), hour_str,
                  font=self.small_font, fill=color1)
        draw.text((self.x(min_str), 8), min_str,
                  font=self.small_font, fill=color1)
        draw.text((self.x(sec_str), 16), sec_str,
                  font=self.small_font, fill=color2)
        draw.text((self.x("SECS"), 24), "SECS",
                  font=self.small_font, fill=color2)

      else:
        draw.text((self.x("HAPPY"), 0), "HAPPY",
                  font=self.small_font, fill=color2)
        draw.text((self.x("NEW"), 8), "NEW",
                  font=self.small_font, fill=color2)
        draw.text((self.x("YEAR!"), 16), "YEAR!",
                  font=self.small_font, fill=color2)

    return 10

  def x(self, text):

    w, h = self.small_font.getsize(text)
    xloc = (self.width - w) / 2

    return xloc
