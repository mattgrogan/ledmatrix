import math

from PIL import Image, ImageChops


class Pattern_Sine(object):

  def __init__(self, width, height):

    self.width = width
    self.height = height

    self.image = Image.new("RGB", (self.width, self.height))
    self.pix = self.image.load()

    self.offset = int(self.height / 2)
    self.scale = int((self.height - 2) / 2)
    self.angle_increment = math.pi / 25.0

    self.x = 0
    self.y = 0
    self.angle = 0.0

  def handle_input(self, command):
      pass


  def draw_frame(self):

    # Turn old point black
    #self.pix[self.x, self.y] = (0, 0, 0)

    # Scroll the image
    if self.x >= self.width:
      self.image = ImageChops.offset(self.image, -1, 0)
      self.pix = self.image.load()
      self.x = self.width - 1

      # Set all pixels in the last row to black
      for i in range(self.height):
        self.pix[self.x, i] = (0, 0, 0)

    # Calculate new point and set the color
    self.y = self.offset + (math.sin(self.angle) * self.scale)
    self.pix[self.x, self.y] = (255, 255, 255)

    # Increment the variables
    self.x += 1
    self.angle += self.angle_increment

    return self.image, 60
