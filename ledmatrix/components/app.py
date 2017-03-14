class App(object):
  """
  Application to show animations or information on the screen
  """

  is_playlist = False
  is_finished = False

  def handle_input(self, command):

    pass

  def draw_frame(self):

    raise NotImplementedError


class Indicator_App(App):
  """
  Application to show information on the screen. This class handles the
  movement between different frames in the same application.
  """

  def __init__(self, device):
    """
    Initialize the item with the device (required for height and width)
    """

    self.device = device
    self._current_frame = 0
    self._frames = []
    self.is_playlist = True
    self.is_finished = False

  def add_frame(self, frame):
    """
    Add a frame to this Application. The frames will be scrolled down and
    then to the left.
    """

    self._frames.append(frame)

  @property
  def current_frame(self):
    """
    Helper to point to the current frame
    """

    if len(self._frames) > self._current_frame:
      return self._frames[self._current_frame]

  def next(self):
    """
    Move to the next frame, or cycle back to the first frame.
    """
    self._current_frame += 1

    if self._current_frame >= len(self._frames):
      self._current_frame = 0
      self.is_finished = True

  def draw_frame(self):
    """
    Move to next frame if required. Draw the current frame.
    """

    self.is_finished = False

    requested_delay = self.current_frame.draw_frame()

    if self.current_frame.is_finished:
      self.current_frame.reset()
      self.next()

    return requested_delay
