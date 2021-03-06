import logging
import time

import requests

import influxdb
import RPi.GPIO as GPIO

DELAY_SECS = 1
PIR_PIN = 26

log = logging.getLogger("ledmatrix")


class PIR(object):

  def __init__(self, dbclient):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    self.dbclient = dbclient

    self.last_state = GPIO.input(PIR_PIN)
    self.last_check = None
    self.last_event = time.time()

    log.info("Started PIR with state: %i" % self.last_state)

  def get_readings(self):

    state = GPIO.input(PIR_PIN)

    if state:
      self.last_event = time.time()

    if state != self.last_state:
      log.info("PIR State change to %i" % state)
      self.last_state = state

    point = {"measurement": "PIR", "fields": {
        "motion": int(state),
        "inactivity_mins": round((time.time() - self.last_event) / 60)
    }}

    try:
      self.dbclient.write_points([point])
    except requests.exceptions.ConnectionError:
      log.critical("Unable to connect to InfluxDB")

  def execute(self):
    if self.last_check is None:
      delay_expired = True  # This is the first run
    else:
      delay_expired = time.time() > (self.last_check + DELAY_SECS)

    if delay_expired:
      self.get_readings()
      self.last_check = time.time()
