import datetime
import rfc822
import urllib2
import xml.etree.ElementTree as ET


class NOAA_Current_Observation(object):
  """
  Represents a connection to weather.gov

  This class handles connections to weather.gov for the current observation. It
  attempts to behave by limiting the number of possible connection attempts.

  :param string url:
    The URL To connect to. Example:
    "http://w1.weather.gov/xml/current_obs/KLGA.xml"

  :param int pickup_period:
    The number of seconds to wait for the next observation. The duration starts
    at the last observation time from weather.gov. Defaults to 60 minutes.

  :param int timeout:
    The number of seconds to timeout after the last connection attempt. Defaults
    to 10 minutes.
  """

  def __init__(self, station, pickup_period=60 * 60, timeout=10 * 60):

    self.station = station
    self.url = "http://w1.weather.gov/xml/current_obs/%s.xml" % station
    self.pickup_period = pickup_period
    self.timeout = timeout

    self.current_obs = {}   # Dict to hold observation data
    self._last_observation = None  # Time of the last observation from XML
    self._last_attempt = None      # Time of the last connection attempt

  def __getitem__(self, name):
    """
    Checks for new data and returns the appropriate value.
    """

    self.update()

    if name in self.current_obs.keys():
      return self.current_obs[name]
    else:
      return None

  @property
  def _timeout_expired(self):
    """
    Determines if the timeout since last attempt has expired.
    """

    # This is the first attempt
    if self._last_attempt is None:
      return True

    # How many seconds since the last attempt?
    delta = (datetime.datetime.now() - self._last_attempt).total_seconds()

    return delta > self.timeout

  @property
  def _pickup_expired(self):
    """
    Determines if the pickup time has expired
    """

    if self._last_observation is None:
      return True

    # How many seconds since the last attempt?
    delta = (datetime.datetime.now() - self._last_observation).total_seconds()

    return delta > self.pickup_period

  def _fetch_data(self):

    # Attempt a connection
    try:
      self._last_attempt = datetime.datetime.now()
      s = urllib2.urlopen(self.url)
    except urllib2.URLError as e:
      print "Unable to update current conditions: %s" % e.reason
      return False

    # Parse the data
    root = ET.fromstring(s.read())
    for child in root:
      self.current_obs[child.tag] = child.text

    # Save the observation time
    last_obs = self.current_obs["observation_time_rfc822"]
    self._last_observation = self.convert_rfc822(last_obs)

    return True

  def update(self, force=False):
    """
    Obtains the latest observation from weather.gov.

    :param bool force:
      Forces a connection to weather.gov irrespective of pickup period and
      timeouts. Defaults to False.
    """

    # Check for good behavior
    if (self._pickup_expired and self._timeout_expired) or force:
      print "Updating weather..."
      self._fetch_data()
      return True
    else:
      print "Skipping weather update."
      return False

  def convert_rfc822(self, date_string):
    """ Helper to convert rfc822 to datetime object """

    date_object = rfc822.parsedate_tz(date_string)
    date_object = rfc822.mktime_tz(date_object)
    date_object = datetime.datetime.fromtimestamp(date_object)

    return date_object
