import random
import time

import Image
import ImageChops
import ImageDraw

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32


class Wander_Image(object):
  """ This class prepares a still image for display on the RGB Matrix """

  def __init__(self, filename, matrix):
    """ Initialize with the filename of the image and a reference to the RGB Matrix """

    self.filename = filename
    self.matrix = matrix

    self.x = 0
    self.y = 0

    # TODO: wrap in try statement
    self.image = Image.open(filename)

    self.image = self.image.resize(
        (128, 128), Image.ANTIALIAS)

  def display(self, duration=10):
    """ Display the image on the matrix for duration seconds """

    elapsed_duration = 0

    # while elapsed_duration < duration:

    while True:

      for x in range(0, 128 - MATRIX_WIDTH):

        offset_image = ImageChops.offset(self.image, -1 * x, 0)
        cropped_image = offset_image.crop((0, 0, 31, 31))

        self.matrix.SetImage(cropped_image.im.id)
        time.sleep(0.025)
        duration += 0.025

      for y in range(0, MATRIX_HEIGHT):

        offset_image = ImageChops.offset(self.image, -1 * x, -1 * y)
        cropped_image = offset_image.crop((0, 0, 31, 31))

        self.matrix.SetImage(cropped_image.im.id)
        time.sleep(0.025)
        duration += 0.025

      for x in range(-1 * x, 0):

        offset_image = ImageChops.offset(self.image, x, -32)
        cropped_image = offset_image.crop((0, 0, 31, 31))

        self.matrix.SetImage(cropped_image.im.id)
        time.sleep(0.025)
        duration += 0.025

      for y in range(y, y + MATRIX_HEIGHT):

        offset_image = ImageChops.offset(self.image, -1 * x, -1 * y)
        cropped_image = offset_image.crop((0, 0, 31, 31))

        self.matrix.SetImage(cropped_image.im.id)
        time.sleep(0.025)
        duration += 0.025

      for x in range(0, 128 - MATRIX_WIDTH):

        offset_image = ImageChops.offset(self.image, -1 * x, -1 * y)
        cropped_image = offset_image.crop((0, 0, 31, 31))

        self.matrix.SetImage(cropped_image.im.id)
        time.sleep(0.025)
        duration += 0.025

      for y in range(y, y + MATRIX_HEIGHT):

        offset_image = ImageChops.offset(self.image, -1 * x, -1 * y)
        cropped_image = offset_image.crop((0, 0, 31, 31))

        self.matrix.SetImage(cropped_image.im.id)
        time.sleep(0.025)
        duration += 0.025

      for x in range(-1 * x, 0):

        offset_image = ImageChops.offset(self.image, x, -1 * y)
        cropped_image = offset_image.crop((0, 0, 31, 31))

        self.matrix.SetImage(cropped_image.im.id)
        time.sleep(0.025)
        duration += 0.025

      self.matrix.Clear()
      time.sleep(2)
