import time

import Image
import ImageDraw

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32


class Still_Image(object):
  """ This class prepares a still image for display on the RGB Matrix """

  def __init__(self, filename, matrix):
    """ Initialize with the filename of the image and a reference to the RGB Matrix """

    self.filename = filename
    self.matrix = matrix

    # TODO: wrap in try statement
    self.image = Image.open(filename)

    self.image = self.image.resize(
        (MATRIX_WIDTH, MATRIX_HEIGHT), Image.ANTIALIAS)

  def display(self, duration=10):
    """ Display the image on the matrix for duration seconds """

    self.matrix.Clear()
    self.matrix.SetImage(self.image.im.id)
    time.sleep(duration)
    self.matrix.Clear()
