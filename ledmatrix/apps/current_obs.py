import time
from data.current_conditions import NOAA_Current_Observation


class Current_Obs_Mapper(object):
  """ Mapper for current observation from NOAA """

  def __init__(self, station):

    self._noaa_current_obs = NOAA_Current_Observation(station)

  def data(self):

    data = {}
    data["icon_name"] = "sunny"
    data["icon_color"] = "#FFFF00"
    data["line1"] = self._noaa_current_obs["temp_f"]
    data["line2"] = time.strftime("%I:%M", time.localtime()).lstrip("0")
    data["line3"] = self._noaa_current_obs["weather"]

    return data
