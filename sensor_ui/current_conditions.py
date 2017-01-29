from __future__ import division

import datetime
import rfc822
import urllib2
import xml.etree.ElementTree as ET

CURRENT_WEATHER_URL = "http://w1.weather.gov/xml/current_obs/KLGA.xml"
REFRESH_SECS = 60 * 60  # Refresh every sixty minutes
# ATTEMPT_TIMEOUT = 60 * 10 # Don't refresh more than every 10 mins


class Current_Conditions(object):

  def __init__(self):

    self._temp_f = None
    self._weather = None
    self._last_updated = None

  @property
  def data_expired(self):
    """ Return true if the data are expired """

    if self._last_updated is None:
      return True

    return self.last_updated > REFRESH_SECS

  @property
  def temp_f(self):
    """ Return the temperature in fahrenheit """

    self.update_weather()
    return self._temp_f

  @property
  def weather(self):

    self.update_weather()
    return self._weather

  @property
  def last_updated(self):
    """ How many seconds since the last update """

    if self._last_updated is None:
      return None

    now = datetime.datetime.now()
    then = self._last_updated

    secs_since_updated = (now - then).total_seconds()

    return round(secs_since_updated)

  def convert_rfc822(self, date_string):
    """ Helper to convert rfc822 to datetime object """

    date_object = rfc822.parsedate_tz(date_string)
    date_object = rfc822.mktime_tz(date_object)
    date_object = datetime.datetime.fromtimestamp(date_object)

    return date_object

  def update_weather(self):

    if self.data_expired:

      print "Updating weather"

      # Pull the XML from NOAA
      s = urllib2.urlopen(CURRENT_WEATHER_URL)
      root = ET.fromstring(s.read())

      # Extract interesting variables

      self._temp_f = root.find("temp_f").text
      self._weather = root.find("weather").text

      last_updated = root.find("observation_time_rfc822").text
      self._last_updated = self.convert_rfc822(last_updated)

      # print (datetime.datetime.now() - last_updated).total_seconds() / 60


if __name__ == "__main__":
  cc = Current_Conditions()
  print cc.temp_f
  print cc.weather
  print "Updated %i minutes ago" % (cc.last_updated / 60)
