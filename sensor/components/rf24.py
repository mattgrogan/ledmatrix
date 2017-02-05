import logging
import time

import requests

import influxdb
from nrf24 import NRF24

log = logging.getLogger("ledmatrix")


class RF24_Sensor(object):

  def __init__(self, dbhost="localhost", dbport=8086, dbname=None):

    # Set up the RF24
    pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7],
             [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

    self.radio = NRF24()
    self.radio.begin(0, 0, 17, 27)

    self.radio.setRetries(15, 15)

    self.radio.setPayloadSize(32)
    self.radio.setChannel(0x60)
    self.radio.setDataRate(NRF24.BR_250KBPS)
    self.radio.setPALevel(NRF24.PA_MAX)

    self.radio.setAutoAck(1)

    self.radio.openWritingPipe(pipes[0])
    self.radio.openReadingPipe(1, pipes[1])

    self.radio.startListening()

    # Set up influxdb
    self.dbclient = influxdb.InfluxDBClient(dbhost, dbport, database=dbname)
    log.info("Started NF24")

  def get_msg(self):

    msg_str = ""

    if self.radio.available():
      while self.radio.available():

        msg = []
        self.radio.read(msg, self.radio.getDynamicPayloadSize())

        for n in msg:

          # Break on null character
          if n == 0:
            break

          if 32 <= n <= 126:
            msg_str += chr(n)

      log.info("Received message %s" % msg_str)

    return msg_str

  def save_value(self, value):

    point = {"measurement": "Soil", "fields": {
        "humidity": value
    }}

    try:
      self.dbclient.write_points([point])
    except requests.exceptions.ConnectionError:
      log.critical("Unable to connect to InfluxDB")

  def execute(self):

    msg = self.get_msg()

    if len(msg) > 0:
      self.save_value(int(msg))
