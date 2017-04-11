import logging
#import urllib2
import requests
import xml.etree.ElementTree as ET

from utils.throttle_mixin import Throttle_Mixin

log = logging.getLogger("ledmatrix")
logging.basicConfig()
log.setLevel(logging.DEBUG)


class NOAA_Current_Observation(Throttle_Mixin):
  """
  This class handles connections to weather.gov for the current observation.
  """

  def __init__(self, station):

    self.station = station
    self.url = "http://w1.weather.gov/xml/current_obs/%s.xml" % station

    self.current_obs = {}   # Dict to hold observation data

    # Use the Mixin to throttle requests
    self.every(60 * 30, self._fetch_data)

  def __getitem__(self, name):
    """
    Checks for new data and returns the appropriate value.
    """

    # Call mixin
    self.run_pending()

    if name in self.current_obs.keys():
      return self.current_obs[name]
    else:
      return ""

  def _fetch_data(self):

    # Attempt a connection
    try:
      r = requests.get(self.url)
    except:
      log.exception("Exception")
      return False

    if r.status_code == requests.codes.ok:
      # Parse the data
      root = ET.fromstring(r.content)
      for child in root:
        self.current_obs[child.tag] = child.text
      return True
    else:
      log.error("Request status code=%i" % r.status_code)
      return False

if __name__ == "__main__":

  cc = NOAA_Current_Observation("KLGA")
  print cc["temp_f"]
  print cc["observation_time"]
