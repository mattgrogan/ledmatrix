import logging
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import influxdb

log = logging.getLogger("ledmatrix")

DELAY_SECS = 60
MCP_PORT = 0

# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0


class Phototransistor(object):
  """ Read from a Phototransistor through the mcp3008 """

  def __init__(self, dbhost="localhost", dbport=8086, dbname=None):

    self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    self.dbclient = influxdb.InfluxDBClient(dbhost, dbport, database=dbname)

    self.last_check = None

  def get_readings(self):

    reading = None
    reading = self.mcp.read_adc(MCP_PORT)

    point = None

    if reading is not None:
      point = {"measurement": "Phototransistor", "fields": {
          "ambient_light": reading
      }}
    else:
      log.critical("Unable to sample ambient light")

    if point is not None:
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
