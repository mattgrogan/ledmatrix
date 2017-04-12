import time
from data.utils.indicator_mapper import Indicator_Data_Map
from data.current_conditions import NOAA_Current_Observation


class Current_Obs_Mapper(Indicator_Data_Map):
  """ Mapper for current observation from NOAA """

  def __init__(self, station):

    self._noaa_current_obs = NOAA_Current_Observation(station)
    self.init()

    self["icon_name"] = "sunny"
    self["icon_color"] = "#FFFF00"
    self["line1"] = self.temp_str
    self["line2"] = lambda: time.strftime(
        "%I:%M", time.localtime()).lstrip("0")
    self["line3"] = lambda: self._noaa_current_obs["weather"]

  def temp_str(self):
    """
    Returns the temperature with decimal point dropped
    """

    try:
      temp = "%iF" % int(float(self._noaa_current_obs["temp_f"]))
    except:
      temp = ""

    return temp
