import time
from menu import Menu


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self, matrix=None):
    """ Initialize the controller """

    self.matrix = matrix

    self.items = Menu()

    self.is_running = True

  @property
  def index(self):
    """ Return the current index """

  def handle_setup(self, message=None):
    pass

  def handle_up(self, message=None):
    self.items.current_item.handle_input("UP")

  def handle_mode(self, message=None):
    self.items.move(1)

  def handle_left(self, message=None):
    self.items.current_item.handle_input("LEFT")

  def handle_enter(self, message=None):
    self.items.current_item.handle_input("ENTER")

  def handle_right(self, message=None):
    self.items.current_item.handle_input("RIGHT")

  def handle_down(self, message=None):
    self.items.current_item.handle_input("DOWN")

  def handle_back(self, message=None):
    pass

  def handle_playpause(self, message=None):
    self.toggle_running()

  def toggle_running(self):
    """ toggle self.is_running """

    if self.is_running():
      self.matrix.clear()

    self.is_running = not self.is_running

  def run(self):
    """ Run the animations """

    if self.is_running:
      requested_delay_ms = self.items.current_item.draw_frame()
      # self.matrix.set_image(image)
    else:
      requested_delay_ms = 25

    return requested_delay_ms
