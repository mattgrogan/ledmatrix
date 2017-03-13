import time
from canvas import canvas

from PIL import Image

from data import NOAA_Current_Observation
from device import Viewport
from drawable import Drawable


class Messages(Drawable):
  """
  Display messages on the screen
  """

  def __init__(self, device, station=None):

    msg = "Hello, world! My name is Matt"
    w, h = self.small_font.getsize(msg)
    w += device.width * 2  # Increase so we scroll on and off the screen
    h = max(h, device.height)
    self.devwidth = device.width

    self.device = Viewport(device, w, h)

    self.station = station
    self._cc = None         # Hold the current conditions

    if self.station is not None:
      self._cc = NOAA_Current_Observation(station)

  def reading(self, field):
    if self._cc is None:
      return ""

    return self._cc[field]

  def build_image(self):

    line1 = self.reading("location")
    line2 = self.reading("weather")
    line3 = self.reading("temperature_string")

    w, h = self.small_font.getsize(line1)

    with canvas(self.device) as draw:
<<<<<<< HEAD
      draw.text((self.devwidth, 20), line1, font=self.small_font)
      #draw.text((self.devwidth, h), line2, font=self.small_font)
      #draw.text((self.devwidth, h * 2), line3, font=self.small_font)

  def draw_frame(self):

    #scrolled = self.device.move_left()

    pix = self.device.image.load()

    sun = [0x020, 0x422, 0x204, 0x0F0,
           0x1F8, 0xDF8, 0x1FB, 0x1F8,
           0x0F0, 0x204, 0x442, 0x040]

    for x in range(12):
      for y in range(12):
        row = surprise_face[y]
        cell = row & (1 << (12 - x - 1))
        pix[x, y] = cell
=======
      draw.text((self.devwidth, 0), line1, font=self.small_font)
      draw.text((self.devwidth, h), line2, font=self.small_font)
      draw.text((self.devwidth, h * 2), line3, font=self.small_font)

  def draw_frame(self):

    scrolled = self.device.move_left()
>>>>>>> master

    if not scrolled:
      self.device.set_position((0, 0))

<<<<<<< HEAD
    self.device.display()
=======
    self.build_image()

    # self.device.display()
>>>>>>> master

    return 5
