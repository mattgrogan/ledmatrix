import time
from components import Indicator_App, Indicator
from info.data import NOAA_Current_Observation


class Weather_App(Indicator_App):

  def __init__(self, device, station):

    super(Weather_App, self).__init__(device)

    self.device = device
    self.station = station
    self.cc = NOAA_Current_Observation(station)

    indicator = Indicator(device)
    indicator.icon("sunny", color="#FFFF00")
    indicator.icon_text(self.temp)
    indicator.line1(self.time, scroll=False)
    indicator.line2(self.long_text)

    self.add_frame(indicator)

    date_frame = Indicator(device)
    date_frame.icon("sunny", color="#FFFF00")
    date_frame.icon_text(self.temp)
    date_frame.line1(self.time, scroll=False)
    date_frame.line2(self.date)

    self.add_frame(date_frame)

  def long_text(self):
    text = self.cc["weather"]
    return text

  def weather(self):
    return self.cc["weather"]

  def temp(self):

    temp = self.cc["temp_f"]

    if temp is not None:
      temp = "%iF" % int(float(temp))  # Drop the decimal point
    else:
      temp = ""

    return temp

  def date(self):
    """ Return date in proper format """

    return time.strftime("%a %b %d", time.localtime())

  def time(self):
    """ Return the time in HH:MM format """

    return time.strftime("%I:%M", time.localtime()).lstrip("0")
