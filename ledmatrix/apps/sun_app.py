import requests
import json
import iso8601
from dateutil import tz

from components import Indicator_App, Icon, Text, NoScroll_Text, Indicator_Frame

URL = "https://api.sunrise-sunset.org/json?lat=40.7127837&lng=-74.0059413&formatted=0&date=today"


class Sun_App(Indicator_App):
  """ Show sun rise and set times """

  def __init__(self, device):

    super(Sun_App, self).__init__(device)

    self.device = device

  def update_data(self):
    """ Grab new data from the url """

    data = requests.get(URL)

    if data.ok:
      sun_data = json.loads(data.content)

      print "The response contains {0} properties".format(len(sun_data))
      print "\n"

      for key, elem in sun_data["results"].items():
        print key
        print elem

      sunrise = sun_data["results"]["sunrise"]
      print "sunrise: " + sunrise

      sunrise = iso8601.parse_date(sunrise)

      print type(sunrise)

      #to_zone = tz.gettz('America/New_York')
      to_zone = tz.tzlocal()

      print sunrise.astimezone(to_zone)
