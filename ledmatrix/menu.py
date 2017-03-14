import random


class Menu(object):
  """
  Handles menu options
  """

  def __init__(self):

    self._current_index = 0
    self._keys = []
    self._items = {}

  def __len__(self):

    return len(self._keys)

  def append(self, name, item):

    self._keys.append(name)
    self._items[name] = item

  @property
  def current_item_name(self):

    if len(self) == 0:
      raise ValueError("You must add menu items to the menu")

    return self._keys[self._current_index]

  @property
  def current_item(self):

    return self._items[self.current_item_name]

  def move(self, step):

    self._current_index = (self._current_index + step) % len(self._keys)

  def move_random(self):

    self._current_index = random.choice(range(len(self._keys)))

    while self.current_item.is_playlist == False:
      self._current_index = random.choice(range(len(self._keys)))

  def next(self):

    self.move(1)

  def prev(self):

    self.move(-1)
