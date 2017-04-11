import time
from data.current_conditions import NOAA_Current_Observation


class Indicator_Data_Map(object):

  def init(self):
    self._items = {}

  def __getitem__(self, key):
    item = self._items[key]
    if callable(item):
      item = item()  # call it if it's a lambda

    return item

  def __setitem__(self, key, val):
    if self._items is None:
      self._items = {}
    self._items[key] = val


class Current_Obs_Mapper(Indicator_Data_Map):
  """ Mapper for current observation from NOAA """

  def __init__(self, station):

    self._noaa_current_obs = NOAA_Current_Observation(station)
    self.init()

    self["icon_name"] = "sunny"
    self["icon_color"] = "#FFFF00"
    self["line1"] = lambda: self._noaa_current_obs["temp_f"]
    self["line2"] = lambda: time.strftime(
        "%I:%M", time.localtime()).lstrip("0")
    self["line3"] = lambda: self._noaa_current_obs["weather"]
