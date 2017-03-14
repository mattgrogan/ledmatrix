import time
from components import Indicator_App, Icon, Text, NoScroll_Text, Indicator_Frame
from info.data import NOAA_Current_Observation


class Weather_App(Indicator_App):

  def __init__(self, device, station):

    super(Weather_App, self).__init__(device)

    self.device = device
    self.station = station
    self.cc = NOAA_Current_Observation(station)

    # Build frames
    sunny = Icon.Icon("sunny", color="#FFFF00")
    temp_text = NoScroll_Text(self.temp)
    time_text = NoScroll_Text(self.time)
    long_text = Text(self.long_text)

    # Weather Frame
    w_frame = Indicator_Frame(device)
    w_frame.add_item(sunny, (1, 1))
    w_frame.add_item(temp_text, (sunny.size[0] + 2, 4))
    w_frame.add_item(long_text, (0, sunny.size[1] + 1))
    w_frame.add_item(time_text, (5, sunny.size[1] + long_text.size[1] + 2))

    self.add_frame(w_frame)
    self.add_frame(Indicator_Frame(device))  # Add a blank frame

  def long_text(self):
    text = self.cc["weather"]
    text += "  Winds "
    text += self.cc["wind_string"]
    text += "  RH: "
    text += self.cc["relative_humidity"]
    text += "%  "
    text += self.cc["observation_time"]
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
