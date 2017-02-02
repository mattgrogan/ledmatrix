# This code handles the user interface for the sensor box
from __future__ import division

import time
from datetime import datetime
import textwrap

import gpiozero
import influxdb
import iso8601  # for date string -> date object
from Adafruit_LED_Backpack import AlphaNum4
from current_conditions import Current_Conditions
from rotary_encoder import RotaryEncoder

INFLUX_HOST = "ledmatrix"
INFLUX_DB = "home"


class Sensor_UI(object):

  def __init__(self):

    self.dbclient = influxdb.InfluxDBClient(
        INFLUX_HOST, 8086, database=INFLUX_DB)

    self.displays = []
    start_addr = 0x70

    for i in range(4):
      addr = start_addr + i
      print "Connecting to %i" % i
      disp = AlphaNum4.AlphaNum4(address=addr)
      disp.begin()
      disp.set_brightness(15)
      disp.clear()
      disp.write_display()
      self.displays.append(disp)

    # For rotary encoder
    self.threshold = 4
    self.counter = 0
    self.last = 1

    # Menu position
    self.menu_items = [self.identify,
                       self.show_temp, self.show_current_conditions]
    self.current_index = 0

    # Current Current_Conditions
    self.current_conditions = Current_Conditions()
    self.current_conditions.update_weather()

    # RGB LED
    #self.led = gpiozero.RGBLED(16, 20, 21)
    # self.led.color(1,0,1)

  def identify(self):
    """ Identify the displays """

    for i, disp in enumerate(self.displays):
      disp.clear()
      disp.print_str(str(i))
      disp.write_display()

  def clear(self):

    for i, disp in enumerate(self.displays):
      disp.clear()

  def show_temp(self):

    self.clear()

    # Write out temp and humidity
    # ---------------------------

    query = """ SELECT
                        "temp_f" AS "temp_f",
                        "humidity" as "humidity"
                    FROM "home"."autogen"."SI7201 Temp+Humidity"
                    ORDER BY DESC
                    LIMIT 1
        """
    rs = self.dbclient.query(query)
    data = list(rs.get_points())
    d = data[0]

    time_string = d["time"]
    now = datetime.utcnow()
    then = iso8601.parse_date(time_string, default_timezone=None)

    then = then.replace(tzinfo=None)

    print "Time string: %s" % d["time"]
    print "Now: %s" % now
    print "Then: %s" % then

    last_update_secs = (now - then).total_seconds()

    if last_update_secs < 120:
      last_update_str = "NOW"
    else:
      last_update_str = "%im" % (last_update_secs / 60)

    temp_f = round(d["temp_f"])
    humidity = round(d["humidity"])

    self.displays[0].print_str("TEMP")
    self.displays[2].print_str("%i f" % temp_f)

    self.displays[1].print_str(last_update_str)
    self.displays[3].print_str("%irh" % humidity)

    for disp in self.displays:
      disp.write_display()

  def show_current_conditions(self):

    self.clear()

    last_updated_str = "%im" % (self.current_conditions.last_updated / 60)
    temp_f_str = "%sF" % (self.current_conditions.temp_f)

    self.displays[0].print_str("LGA")
    self.displays[1].print_str(last_updated_str)
    self.displays[2].print_number_str(temp_f_str)
    self.displays[3].print_str(self.current_conditions.weather)

    for disp in self.displays:
      disp.write_display()

    # Trying out string wrapping
    weather = self.current_conditions.build_string()

    print textwrap.wrap(weather, 8)


  def rotary_changed(self, value):

    if value != self.last:
      self.counter = 0  # Reset counter if different direction

    self.last = value
    self.counter += value

    if abs(self.counter) >= self.threshold:
      if self.counter > 0:
        self.move(1)
      else:
        self.move(-1)
      self.counter = 0

  def move(self, step):

    self.current_index += step

    if self.current_index >= len(self.menu_items):
      self.current_index = 0
    elif self.current_index < 0:
      self.current_index = len(self.menu_items) - 1

    print "current index: %i" % self.current_index

    self.menu_items[self.current_index]()




if __name__ == "__main__":

  rotary_btn = gpiozero.Button(6)
  rc = RotaryEncoder(19, 13)

  ui = Sensor_UI()
  rc.when_rotated = ui.rotary_changed

  while True:
    time.sleep(0.01)

  # ui.identify()
  # rotary_btn.wait_for_press()
  # ui.show_temp()
