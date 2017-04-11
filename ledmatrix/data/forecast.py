import requests
import json
import logging

from utils.throttle_mixin import Throttle_Mixin

log = logging.getLogger("ledmatrix")
logging.basicConfig()
log.setLevel(logging.DEBUG)


class NOAA_Forecast(Throttle_Mixin):
  """ Obtain a forecast from weather.gov """

  def __init__(self, lat, lon, timeout=2):
    """
    lat, lon: coordinates of the forecast
    """

    self._opts = {
        "lat": lat,
        "lon": lon,
        "FcstType": "json"
    }

    self.timeout = timeout

    self.url = "http://forecast.weather.gov/MapClick.php"

    self._results = {}

    self.every(60 * 60, self._fetch_data)

  def __getitem__(self, key):
    """ Retrieve an item, if it doesn't exist, return an empty set """

    # Call Mixin
    self.run_pending()

    if key in self._results.keys():
      data = self._results[key]
    else:
      data = ""

    return data

  def _fetch_data(self):

    try:
      r = requests.get(self.url, params=self._opts, timeout=self.timeout)
    except:
      log.exception("Exception")
      return False

    if r.status_code == requests.codes.ok:
      self._results = json.loads(r.content)
      return True
    else:
      self._results = {}
      return False


class NOAA_Forecast_Adapter(object):
  """
  Adapter to make it easier to get forecast data
  """

  def __init__(self, lat, lon, timeout=2):
    self._noaa_forecast = NOAA_Forecast(lat, lon, timeout)

  def __getitem__(self, key):

    result = {}

    # Use the index of the various fields
    assert key in range(12)

    time_fields = ["startPeriodName", "startValidTime", "tempLabel"]
    data_fields = ["temperature", "weather", "iconLink", "text"]

    for field in time_fields:
      result[field] = self._noaa_forecast["time"][field][key]

    for field in data_fields:
      result[field] = self._noaa_forecast["data"][field][key]

    return result


if __name__ == "__main__":
  f = NOAA_Forecast_Adapter(40.7127837,  -74.0059413)

  import pprint
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(f[1])
