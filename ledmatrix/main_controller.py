import time


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self, matrix=None):
    """ Initialize the controller """

    self.matrix = matrix

    self.menu_items = []
    self.current_index = 0
    self.is_running = True

  def handle_setup(self, message=None):
    pass

  def handle_up(self, message=None):
    self.current_item.handle_input("UP")

  def handle_mode(self, message=None):
    self.move(1)

  def handle_left(self, message=None):
    self.current_item.handle_input("LEFT")

  def handle_enter(self, message=None):
    self.current_item.handle_input("ENTER")

  def handle_right(self, message=None):
    self.current_item.handle_input("RIGHT")

  def handle_down(self, message=None):
    self.current_item.handle_input("DOWN")

  def handle_back(self, message=None):
    pass

  def handle_playpause(self, message=None):
    self.toggle_running()

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
      self.matrix.clear()
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

    if self.is_running:
      image, requested_delay_ms = self.current_item.draw_frame()
      self.matrix.set_image(image)
    else:
      requested_delay_ms = 25

    return requested_delay_ms
