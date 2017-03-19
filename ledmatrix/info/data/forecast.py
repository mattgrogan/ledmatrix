import urllib2
import json


class NOAA_Forecast_Result(object):
  # TODO: I think I would prefer this to be a dictionary...

  def __init__(self):

    self.period_name = ""
    self.temp_label = ""
    self.temp = ""
    self.pop = ""
    self.weather = ""
    self.text = ""

  def __str__(self):

    text = self.period_name + " "
    text += self.temp + " " + self.temp_label + " "
    text += self.pop if self.pop is not None else ""
    text += " " + self.weather + " \n"
    text += self.text

    return text


class NOAA_Forecast(object):

  def __init__(self, lat, lon):
    """
    Obtain and parse the NOAA Forecast at www.weather.gov
    """

    self._lat = lat
    self._lon = lon
    self.url = "http://forecast.weather.gov/MapClick.php?lat=%f&lon=%f&FcstType=json" % (
        lat, lon)

  def _fetch_data(self):

    # Attempt a connection
    try:
      s = urllib2.urlopen(self.url)
    except urllib2.URLError as e:
      print "Unable to update current conditions: %s" % e.reason
      return False

    self._data = json.load(s)

  def data(self, period):

    f = NOAA_Forecast_Result()

    f.period_name = self._data["time"]["startPeriodName"][period]
    f.temp_label = self._data["time"]["tempLabel"][period]
    f.temp = self._data["data"]["temperature"][period]
    f.pop = self._data["data"]["pop"][period]
    f.weather = self._data["data"]["weather"][period]
    f.text = self._data["data"]["text"][period]

    return f


if __name__ == "__main__":

  f = NOAA_Forecast(40.78, -73.87)
  f._fetch_data()
  print f.data(2)
