from __future__ import division

import math
import os
import time
from canvas import canvas

import randomcolor
from PIL import Image, ImageChops, ImageDraw, ImageFont

from drawable import Drawable


class Countdown(Drawable):
  """ Show the time until NYE """

  def __init__(self, device, until=time.time() + 600, msg=None):
    """
    Display a countdown. Fun for New Year's Eve!

    :param Device device:
      The device to write to.

    :param datetime/int/float until:
      How long to count down. Should be struct_time in local time or seconds
      since the epoch.

      Example:
        time.strptime("01 Jan 18", "%d %b %y")
        time.time() + 600


    :param string msg:
      Message to display afterwards
    """

    # TODO: Add the message!!!

    self.device = device
    self.until = None
    self.msg = msg

    if type(until) is time.struct_time:
      # Convert to seconds from the epoch
      self.until = time.mktime(until)
    elif type(until) is int or type(until is float):
      # Hopefully this is seconds since the epoch
      self.until = until
    else:
      raise ValueError("Invalid value")

    self._col = []
    self.prev_time = None

    self.width = device.width
    self.height = device.height

  @property
  def seconds_remaining(self):
    """
    Returns the number of seconds remaing in the countdown
    """

    #nye = time.mktime(time.strptime("04 Feb 17", "%d %b %y"))
    return self.until - time.mktime(time.localtime())

  def draw_countdown(self):
    """ Countdown has not expired yet """

    with canvas(self.device) as draw:

      color1 = "#709fea"
      color2 = "#88fc95"

      hours = math.floor(self.seconds_remaining / 60 / 60)
      mins = math.floor(self.seconds_remaining / 60)
      secs = round(self.seconds_remaining, 0)

      hour_str = "%i hrs" % hours
      min_str = "%i min" % mins
      sec_str = "%i" % secs

      draw.text((self.x(hour_str), 0), hour_str,
                font=self.small_font, fill=color1)
      draw.text((self.x(min_str), 8), min_str,
                font=self.small_font, fill=color1)
      draw.text((self.x(sec_str), 16), sec_str,
                font=self.small_font, fill=color2)
      draw.text((self.x("SECS"), 24), "SECS",
                font=self.small_font, fill=color2)

  def draw_finale(self):

    with canvas(self.device) as draw:

      color1 = "#709fea"
      color2 = "#88fc95"

      draw.text((self.x("HAPPY"), 0), "HAPPY",
                font=self.small_font, fill=color2)
      draw.text((self.x("NEW"), 8), "NEW",
                font=self.small_font, fill=color2)
      draw.text((self.x("YEAR!"), 16), "YEAR!",
                font=self.small_font, fill=color2)

  def draw_frame(self):
    """ Draw the time on the screen """

    if self.seconds_remaining > 0:
      self.draw_countdown()
    else:
      self.draw_finale()

    return 10

  def x(self, text):

    w, h = self.small_font.getsize(text)
    xloc = (self.width - w) / 2

    return xloc
