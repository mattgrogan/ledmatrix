import time
from canvas import canvas

import randomcolor

from data import NOAA_Current_Observation
from drawable import Drawable


class Clock(Drawable):
  """
  The Clock will show the time, date, and temperature.

  :param Device device:
    The device to write to.

  :param string station:
    NOAA weather station to obtain temperature from.
  """

  def __init__(self, device, station=None):

    self.device = device
    self.station = station
    self._cc = None         # Hold the current conditions

    self._col = []

    self.prev_time = None

    if self.station is not None:
      self._cc = NOAA_Current_Observation(station)

  @property
  def time(self):
    """ Return the time in HH:MM format """

    return time.strftime("%I:%M", time.localtime()).lstrip("0")

  @property
  def day(self):
    """ Return the date in DDD format """

    return time.strftime("%a", time.localtime())

  @property
  def date(self):
    """ Return the date in MMM DD format """

    return time.strftime("%b %d", time.localtime())

  @property
  def temp(self):
    """ Return the temperature if available """

    # Are we checking temperature?
    if self._cc is None:
      return ""

    temp = self._cc["temp_f"]

    if temp is not None:
      temp = "%iF" % int(float(temp))  # Drop the decimal point
    else:
      temp = ""

    return temp

  def randomize_colors(self, time=None, force=False):
    """ Pick some random colors """

    # Only change the colors if time has changed, otherwise
    # its distracting
    if time != self.prev_time or force:

      rand_color = randomcolor.RandomColor()
      self._col = rand_color.generate(count=3)

      self.prev_time = time

  def handle_input(self, command):

    if command == "ENTER":
      self.randomize_colors(force=True)

  def draw_frame(self):
    """ Draw the time on the screen """

    with canvas(self.device) as draw:

      # Get new colors if the time has changed
      self.randomize_colors(self.time)

      # Center the time
      w, h = self.small_font.getsize(self.time)
      xloc = (self.device.width - w) / 2

      # Draw the time
      draw.text((xloc, 2), self.time, font=self.small_font, fill=self._col[0])

      # Draw the day
      w, h = self.small_font.getsize(self.day)
      draw.text((1, 12), self.day, font=self.small_font, fill=self._col[1])

      # Draw the temperature on the same line
      draw.text((w + 5, 12), self.temp,
                font=self.small_font, fill=self._col[2])

      # Draw the date
      draw.text((1, 20), self.date, font=self.small_font, fill=self._col[1])

    return 1000
