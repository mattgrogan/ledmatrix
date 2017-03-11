import logging
import time

import requests

import influxdb
import smbus

log = logging.getLogger("ledmatrix")

DELAY_SECS = 60 # Run only once every sixty seconds
HUMIDITY_ADDR = 0xF5
TEMP_ADDR = 0xF3

class SI7201(object):
  """ SI7201 Temperature and humidity sensor """

  def __init__(self, i2c_addr=0x40, dbhost="localhost", dbport=8086, dbname=None):

    self.i2c_addr = i2c_addr
    self.bus = smbus.SMBus(1)
    self.dbclient = influxdb.InfluxDBClient(dbhost, dbport, database=dbname, timeout=10)
    self.last_check = None

  def write_byte(self, byte):

    try:
      self.bus.write_byte(self.i2c_addr, byte)
    except IOError:
      log.critical("Unable to write to SI7201 at 0x%02x" % self.i2c_addr)

  def read_byte(self):

    data = None

    try:
      data = self.bus.read_byte(self.i2c_addr)
    except IOError:
      log.critical("Unable to read from SI7201 at 0x%02x" % self.i2c_addr)

    return data

  def read_sensor_value(self, address):

    self.write_byte(address)
    time.sleep(0.3)

    # Read the two byes back
    data0 = self.read_byte()
    data1 = self.read_byte()

    return (data0, data1)

  def get_readings(self):
    """ Get the readings from the sensor """

    humidity = None
    temp_c = None
    temp_f = None
    point = None

    log.info("Taking humidity reading")
    h_data0, h_data1 = self.read_sensor_value(HUMIDITY_ADDR)
    log.info("Finished humidity reading")

    # Convert the data
    if h_data0 is not None and h_data1 is not None:
      humidity = ((h_data0 * 256 + h_data1) * 125 / 65536.0) - 6

    time.sleep(0.3)

    log.info("Taking temp reading")
    t_data0, t_data1 = self.read_sensor_value(TEMP_ADDR)
    log.info("Finished temp reading")

    # Convert data
    if t_data0 is not None and t_data1 is not None:
      temp_c = ((t_data0 * 256 + t_data1) * 175.72 / 65536.0) - 46.85
      temp_f = temp_c * 9 / 5 + 32

    if humidity is not None and temp_c is not None and temp_f is not None:
      point = {"measurement": "SI7201 Temp+Humidity", "fields": {
          "humidity": humidity,
          "temp_c": temp_c,
          "temp_f": temp_f
      }}
    else:
      log.critical("At least one measurement is None")

    if point is not None:
      try:
	log.info("Trying to write to influxdb")
        self.dbclient.write_points([point])
      except requests.exceptions.ConnectionError:
        log.critical("Unable to connect to InfluxDB")

    log.info("Finished with temp and humidity readings")

  def execute(self):

    if self.last_check is None:
      log.info("Taking first temperature reading")
      delay_expired = True # This is the first run
    else:
      delay_expired = time.time() > (self.last_check + DELAY_SECS)

    if delay_expired:
      log.info("Taking reading...")
      self.get_readings()
      self.last_check = time.time()
    else:
      log.info("Skipping reading")
