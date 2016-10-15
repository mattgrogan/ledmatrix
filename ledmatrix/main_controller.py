import time

import lirc


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self):
    """ Initialize the controller """

    # Initialize the remote control
    self.remote_controller = lirc.init(
        "ledmatrix", "./lircrc", blocking=False)

    self.menu_items = []
    self.current_index = 0

  @property
  def current_item(self):
    """ Return the current item """

    if len(self.menu_items) == 0:
      raise ValueError("You must add menu items to the controller")

    return self.menu_items[self.current_index]

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

    while True:

      requested_delay = self.current_item.draw_frame()

      time.sleep(requested_delay)

      code = lirc.nextcode()

      if len(code) > 0 and code[0] == u"KEY_RIGHT":
        self.current_item.move(1)
      elif len(code) > 0 and code[0] == u"KEY_LEFT":
        self.current_item.move(-1)
      elif len(code) > 0 and code[0] == u"KEY_DOWN":
        self.move(1)
      elif len(code) > 0 and code[0] == u"KEY_UP":
        self.move(-1)
