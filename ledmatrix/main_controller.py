import time

import lirc
from remote_control import Remote_Control

TICK_SECS = 0.005


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self, matrix):
    """ Initialize the controller """

    self.matrix = matrix

    self.rc = Remote_Control()
    self.rc.register(u"KEY_STOP", self, self.handle_stop)
    self.rc.register(u"KEY_UP", self, self.handle_up)
    self.rc.register(u"KEY_DOWN", self, self.handle_down)
    self.rc.register(u"KEY_LEFT", self, self.handle_left)
    self.rc.register(u"KEY_RIGHT", self, self.handle_right)

    self.menu_items = []
    self.current_index = 0
    self.is_running = True

  def handle_stop(self, message=None):
    self.toggle_running()

  def handle_up(self, message=None):
    self.move(-1)

  def handle_down(self, message=None):
    self.move(1)

  def handle_left(self, message=None):
    self.current_item.move(-1)

  def handle_right(self, message=None):
    self.current_item.move(1)

  @property
  def current_item(self):
    """ Return the current item """

    if len(self.menu_items) == 0:
      raise ValueError("You must add menu items to the controller")

    return self.menu_items[self.current_index]

  def toggle_running(self):
    """ toggle self.is_running """

    if self.is_running:
      self.is_running = False
      self.matrix.Clear()
    else:
      self.is_running = True

  def add_menu_item(self, menu_item):
    """ Add a menu item to the list """

    self.menu_items.append(menu_item)

  def move(self, step=1):
    """ Move to next menu item """

    self.current_index += step

    if self.current_index >= len(self.menu_items):
      self.current_index = 0
    elif self.current_index < 0:
      self.current_index = len(self.menu_items) - 1

  def run(self):
    """ Run the animations """

    current_delay = 0.0
    requested_delay = 0.0

    while True:

      received_cmd = self.rc.read_command()
      delay_timeout = current_delay >= requested_delay

      if self.is_running and (received_cmd or delay_timeout):
        image, requested_delay = self.current_item.draw_frame()
        self.matrix.SetImage(image.im.id)
        current_delay = 0.0
      else:
        current_delay += TICK_SECS

      time.sleep(TICK_SECS)
