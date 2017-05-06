import time
import logging

from menu import Menu
log = logging.getLogger("ledmatrix")


class LEDMatrix_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self):
    """ Initialize the controller """

    self.items = Menu()
    self.is_running = True

  def handle_setup(self, message=None):
    pass

  def handle_up(self, message=None):
    self.items.current_item.handle_input("UP")

  def handle_mode(self, message=None):
    self.items.next()

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

    if self.is_running:
      # self.matrix.clear()
      self.items.current_item.device.clear()
      # TODO: This is a bug. Make sure the controller
      # can tell the ui to clear the matrix.

    self.is_running = not self.is_running

  def run(self):
    """ Run the animations """

    if self.is_running:
      requested_delay_ms = self.items.current_item.draw_frame()
      if self.items.current_item.is_finished:
        self.items.move_random()
        log.info("Starting: %s", self.items.current_item_name)
    else:
      requested_delay_ms = 25

    return requested_delay_ms
