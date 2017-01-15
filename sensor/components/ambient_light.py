import logging
import time

import requests

import Adafruit_VCNL40xx
import influxdb

log = logging.getLogger("ledmatrix")

DELAY_SECS = 60  # Delay between measurements


class Ambient_Light_Sensor(object):

  def __init__(self, dbhost="localhost", dbport=8086, dbname=None):

    self.dbclient = influxdb.InfluxDBClient(dbhost, dbport, database=dbname)
    self.last_check = None

  def get_readings(self):

    proximity = None
    ambient = None

    try:
      vcnl = Adafruit_VCNL40xx.VCNL4010(address=0x13, busnum=1)
      proximity = vcnl.read_proximity()
      ambient = vcnl.read_ambient()
    except:
      log.critical("Unable to read from VCNL4010")

    prox_point = {"measurement": "proximity", "fields": {"value": proximity}}
    amb_point = {"measurement": "ambient_light", "fields": {"value": ambient}}

    if proximity is not None and ambient is not None:
      try:
        self.dbclient.write_points([prox_point, amb_point])
      except requests.exceptions.ConnectionError:
        log.critical("VCNL4010: Unable to connect to InfluxDB")

  def execute(self):

    if self.last_check is None:
      delay_expired = True  # This is the first run
    else:
      delay_expired = time.time() > (self.last_check + DELAY_SECS)

    if delay_expired:
      self.get_readings()
      self.last_check = time.time()
