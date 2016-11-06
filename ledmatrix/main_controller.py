import time

TICK_SECS = 0.005


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self, matrix):
    """ Initialize the controller """

    self.matrix = matrix

    self.menu_items = []
    self.current_index = 0
    self.is_running = True

    self.current_delay = 0.0
    self.requested_delay = 0.0

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

  def run(self, rc):
    """ Run the animations """

    received_cmd = rc.read_command()
    delay_timeout = self.current_delay >= self.requested_delay

    if self.is_running and (received_cmd or delay_timeout):
        image, self.requested_delay = self.current_item.draw_frame()
        self.matrix.SetImage(image.im.id)
        self.current_delay = 0.0
    else:
        self.current_delay += TICK_SECS

    return TICK_SECS
