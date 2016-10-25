import time

import lirc

TICK_SECS = 0.005


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self):
    """ Initialize the controller """

    # Initialize the remote control
    self.remote_controller = lirc.init(
        "ledmatrix", "./lircrc", blocking=False)

    self.menu_items = []
    self.current_index = 0
    self.is_running = True

    self.null_player = None

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

      if current_delay >= requested_delay:
        requested_delay = self.current_item.draw_frame()
        current_delay = 0.0
      else:
        current_delay += TICK_SECS

      time.sleep(TICK_SECS)

      code = lirc.nextcode()

      if len(code) > 0 and code[0] == u"KEY_RIGHT":
        self.current_item.move(1)
      elif len(code) > 0 and code[0] == u"KEY_LEFT":
        self.current_item.move(-1)
      elif len(code) > 0 and code[0] == u"KEY_DOWN":
        self.move(1)
      elif len(code) > 0 and code[0] == u"KEY_UP":
        self.move(-1)
      elif len(code) > 0 and code[0] == u"KEY_STOP":
        self.toggle_running()
      elif len(code) > 0 and code[0] == u"KEY_ENTER":
        self.is_running = True
