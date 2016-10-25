import time
import urllib2
import xml.etree.ElementTree as ET

import randomcolor
from message_player import Message_Player

CURRENT_WEATHER_URL = "http://w1.weather.gov/xml/current_obs/KLGA.xml"
REFRESH_SECS = 60 * 10


class Weather_Playlist(object):
  """ Download and show the weather """

  def __init__(self, matrix, width, height):

    self.matrix = matrix
    self.width = width
    self.height = height

    self.last_updated = None

    self.current_weather_string = ""

    self.message_player = Message_Player(self.matrix, self.width, self.height)

  def update_weather(self):
    """ Download the weather from noaa """

    s = urllib2.urlopen(CURRENT_WEATHER_URL)
    root = ET.fromstring(s.read())

    weather = root.find("weather").text
    wind = "Wind " + root.find("wind_string").text
    temp = root.find("temperature_string").text
    visibility = "Visibility " + root.find("visibility_mi").text + " miles"
    last_updated = root.find("observation_time").text

    self.current_weather_string = temp + " " + weather + \
        " " + wind + " " + visibility + " " + last_updated

    rand_color = randomcolor.RandomColor()
    col = rand_color.generate()[0]

    self.message_player.start(self.current_weather_string, color=col)

    self.last_updated = time.time()

  def move(self, step=1):

    pass

  def draw_frame(self):

    if time.time() - self.last_updated >= REFRESH_SECS:
      self.update_weather()

    requested_delay = self.message_player.draw_frame()
    return requested_delay
