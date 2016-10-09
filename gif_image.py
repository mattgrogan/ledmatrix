import time

import Image
import ImageDraw

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32


class Gif_Image(object):
  """ This class prepares a gif image for display on the RGB Matrix """

  def __init__(self, filename, matrix):
    """ Initialize with the filename of the image and a reference to the RGB Matrix """

    self.filename = filename
    self.matrix = matrix

    # TODO: wrap in try statement
    self.image = Image.open(filename)
    # self.image.load()

    # Resize if necessary
    # if self.image.size != (MATRIX_WIDTH, MATRIX_HEIGHT):
    #  self.image = self.image.resize(
    #      (MATRIX_WIDTH, MATRIX_HEIGHT), Image.ANTIALIAS)

    # Make sure it's RGB
    #self.image = self.image.convert("RGB")

  def display(self, duration=10):
    """ Display the image on the matrix for duration seconds. Note that this is
    the minimum duration: if the animation runs longer, it will continue until
    the current loop is completed. """

    current_frame = 0
    elapsed_duration = 0

    while True:

      image_copy = self.image.copy()

      # Find the time encoded in the gif (milliseconds)
      try:
        frame_duration_ms = image_copy.info["duration"]
      except KeyError:
        frame_duration_ms = 25

      # Show the image
      self.matrix.SetImage(image_copy.im.id)
      time.sleep(frame_duration_ms / 1000.0)

      elapsed_duration += (frame_duration_ms / 1000.0)
      current_frame = current_frame + 1

      # Is there another frame?
      try:
        self.image.seek(current_frame)  # In the original image
      except EOFError:
        # Have we exceeded the duration?
        if elapsed_duration >= duration:
          break
        else:
          current_frame = 0
          self.image.seek(current_frame)  # In the original image

    self.matrix.Clear()
