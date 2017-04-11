import time
from components import Indicator_App, Indicator
from data.current_conditions import NOAA_Current_Observation


class Weather_App(Indicator_App):

  def __init__(self, device, station):

    super(Weather_App, self).__init__(device)

    self.device = device
    self.station = station
    self.cc = NOAA_Current_Observation(station)
    self._last_temp = ""

    self.indicator = Indicator(device)
    self.indicator.icon("sunny", color="#FFFF00")
    self.indicator.icon_text(self.temp)
    self.indicator.line1(self.time, scroll=False)
    self.indicator.line2(self.long_text)

    self.add_frame(self.indicator)

    # date_frame = Indicator(device)
    # date_frame.icon("sunny", color="#FFFF00")
    # date_frame.icon_text(self.temp)
    # date_frame.line1(self.time, scroll=False)
    # date_frame.line2(self.date)
    #
    # self.add_frame(date_frame)

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

    if temp == self._last_temp:
      # Data has been updated
      self.indicator.reset(scroll_in=True)

    return temp

  def date(self):
    """ Return date in proper format """

    return time.strftime("%a %b %d", time.localtime())

  def time(self):
    """ Return the time in HH:MM format """

    return time.strftime("%I:%M", time.localtime()).lstrip("0")
