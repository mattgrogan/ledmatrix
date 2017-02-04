import random
import urllib2
from StringIO import StringIO

from PIL import Image

from device import Viewport
from drawable import Drawable

MODE_LIMIT = 100


class Photo_Image(Drawable):

  def __init__(self, device):

    #url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Portrait_of_young_man_by_Sandro_Botticelli_-_Louvre.jpg/176px-Portrait_of_young_man_by_Sandro_Botticelli_-_Louvre.jpg"
    #url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/St_Vitus_Cathedral_-_Stained_glass_%28retouch%29.jpg/320px-St_Vitus_Cathedral_-_Stained_glass_%28retouch%29.jpg"
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Monumentvalley.jpg/320px-Monumentvalley.jpg"
    im = Image.open(StringIO(urllib2.urlopen(url).read()))

    # im = Image.open("C:\Users\Matt\Documents\docs\photos\unnamed.jpg")
    im = im.convert(device.mode)

    x, y = im.size

    self.device = Viewport(device, x, y, im)

    self._position = (50, 50)
    self.x_speed = 0.75
    self.y_speed = 1.25

    self.device.set_position(self._position)

  def update_position(self):

    x, y = self._position

    # Move according to the speed
    x = int(round(x + self.x_speed))
    y = int(round(y + self.y_speed))

    left, top, right, bottom = self.device.crop_box((x, y))

    # Check for bouncing
    if not 0 <= left <= right <= self.device.width:
      self.x_speed *= -1
    if not 0 <= top <= bottom <= self.device.height:
      self.y_speed *= -1

    self._position = (x, y)

  def handle_input(self, command):

    x, y = self._position

    if command == "UP":
      y -= 1
    elif command == "DOWN":
      y += 1
    elif command == "LEFT":
      x -= 1
    elif command == "RIGHT":
      x += 1

    self._position = (x, y)

  def draw_frame(self):

    self.update_position()

    self.device.set_position(self._position)
    self.device.display()

    return 250
