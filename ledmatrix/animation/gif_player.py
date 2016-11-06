import PIL.Image as Image


class Gif_Player(object):
  """ Draw a single gif image """

  def __init__(self, filename):
    """ Open filename as the GIF """

    self.filename = filename
    self.image = None
    self.time_played_ms = 0
    self.timeout_ms = None
    self.eof = True
    self.current_frame = 0

  @property
  def is_finished(self):
    """ We're finished if we're at the eof and we've passed the timeout """

    if self.timeout_ms is None:
      is_finished = self.eof
    elif self.eof and self.time_played_ms >= self.timeout_ms:
      is_finished = True
    else:
      is_finished = False

    return is_finished

  def start(self, timeout_ms=None):
    """ Reset to the beginning """

    self.timeout_ms = timeout_ms
    self.image = Image.open(self.filename)
    self.time_played_ms = 0
    self.eof = False
    self.current_frame = 0

  def draw_frame(self):
    """ Draw a single frame and return the requested delay """

    image_copy = self.image.copy()

    # Find the encoded duration in milliseconds
    try:
      frame_duration_ms = image_copy.info["duration"]
    except KeyError:
      frame_duration_ms = 25

    self.current_frame += 1

    # Seek to the current frame, if it exists
    try:
      self.image.seek(self.current_frame)
    except EOFError:
      self.current_frame = 0
      self.image.seek(self.current_frame)
      self.eof = True

    self.time_played_ms += frame_duration_ms

    return image_copy, frame_duration_ms
