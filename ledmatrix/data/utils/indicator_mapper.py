class Indicator_Data_Map(object):

  def init(self):
    self._items = {}

  def __getitem__(self, key):
    item = self._items[key]
    if callable(item):
      item = item()  # call it if it's a lambda

    # Always cast to string
    item = str(item)

    return item

  def __setitem__(self, key, val):
    if self._items is None:
      self._items = {}
    self._items[key] = val
