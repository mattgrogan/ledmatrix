from PIL import Image

from device import Viewport
from drawable import Drawable


class Photo_Image(Drawable):

  def __init__(self, device):

    im = Image.open("C:\Users\Matt\Documents\docs\photos\unnamed.jpg")
    im = im.convert(device.mode)

    self.device = Viewport(device, 128, 128, im)

    self._position = (0, 0)

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

    self.device.set_position(self._position)
    self.device.display()

    return 25
