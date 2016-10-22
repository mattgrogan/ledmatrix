class Null_Player(object):
  """ Clear the screen """

  def __init__(self, matrix):
    """ Initialize the player """

    self.matrix = matrix

  def draw_frame(self):
    """ Clear the matrix """

    self.matrix.Clear()

    return 0.025  # Return a short requested delay
