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

    self.null_player = None

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

    if self.null_player is None:
      raise ValueError("You must add a null player to the controller")

    if self.is_running:
      item = self.menu_items[self.current_index]
    else:
      item = self.null_player

    return item

  def toggle_running(self):
    """ toggle self.is_running """

    if self.is_running:
      self.is_running = False
    else:
      self.is_running = True

  def add_null_player(self, null_player):
    """ Add a null player """

    self.null_player = null_player

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

      if self.rc.read_command() or current_delay >= requested_delay:
        image, requested_delay = self.current_item.draw_frame()

        if image is not None:
          self.matrix.SetImage(image.im.id)
        current_delay = 0.0
      else:
        current_delay += TICK_SECS

      time.sleep(TICK_SECS)
