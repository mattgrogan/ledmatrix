import logging
import time

import requests

import influxdb
import smbus

log = logging.getLogger("ledmatrix")


class SI7201(object):
  """ SI7201 Temperature and humidity sensor """

  def __init__(self, i2c_addr=0x40, dbhost="localhost", dbport=8086, dbname=None):

    self.i2c_addr = i2c_addr
    self.bus = smbus.SMBus(1)
    self.dbclient = influxdb.InfluxDBClient(dbhost, dbport, database=dbname)

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

  def execute(self):

    humidity = None
    temp_c = None
    temp_f = None

    # Query for relative humidity
    self.write_byte(0xF5)
    time.sleep(0.3)

    # Read the two byes back
    data0 = self.read_byte()
    data1 = self.read_byte()

    # Convert the data
    if data0 is not None and data1 is not None:
      humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

    time.sleep(0.3)

    # Select temperature NO HOLD master mode
    self.write_byte(0xF3)
    time.sleep(0.3)

    # Read data back
    data0 = self.read_byte()
    data1 = self.read_byte()

    # Convert data
    if data0 is not None and data1 is not None:
      temp_c = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
      temp_f = temp_c * 9 / 5 + 32

    point = {"measurement": "SI7201 Temp+Humidity", "fields": {
        "humidity": humidity,
        "temp_c": temp_c,
        "temp_f": temp_f
    }}

    try:
      self.dbclient.write_points([point])
    except requests.exceptions.ConnectionError:
      log.critical("Unable to connect to InfluxDB")
