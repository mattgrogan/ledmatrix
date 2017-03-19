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
