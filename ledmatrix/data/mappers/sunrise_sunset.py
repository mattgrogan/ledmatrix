import time
from data.utils.indicator_mapper import Indicator_Data_Map
from data.sunrise_sunset import Sunrise_Sunset


class Sunrise_Mapper(Indicator_Data_Map):
  """ Mapper for sunrise and sunset data """

  def __init__(self, lat, lng):

    self._data = Sunrise_Sunset(lat, lng)
    self.init()

    text = lambda: "{0} RISE - {1} SET".format(
        self._data["sunrise"].strftime("%I:%M %p").lstrip("0"),
        self._data["sunset"].strftime("%I:%M %p").lstrip("0")
    )

    self["icon_name"] = "sunny"
    self["icon_color"] = "#FFFF00"
    self["line1"] = ""
    self["line2"] = lambda: time.strftime(
        "%I:%M", time.localtime()).lstrip("0")
    self["line3"] = text
