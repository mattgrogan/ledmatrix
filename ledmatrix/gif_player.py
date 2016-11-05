import Image


class Gif_Player(object):
  """ Draw a single gif image """

  def __init__(self, filename, matrix):
    """ Open filename as the GIF """

    self.filename = filename
    self.matrix = matrix

    self.image = Image.open(filename)

    self.current_frame = 0
    self.eof = False

  def draw_frame(self):
    """ Draw a single frame and return the requested delay """

    self.eof = False

    image_copy = self.image.copy()

    # Find the encoded duration in milliseconds
    try:
      frame_duration = image_copy.info["duration"] / 1000.0
    except KeyError:
      frame_duration = 25 / 1000.0

    # Show the image
    self.matrix.SetImage(image_copy.im.id)

    self.current_frame += 1

    # Seek to the current frame, if it exists
    try:
      self.image.seek(self.current_frame)
    except EOFError:
      self.current_frame = 0
      self.image.seek(self.current_frame)
      frame_duration = "EOF"

    return frame_duration
