import time
import influxdb
import smbus

class SI7201(object):
  """ SI7201 Temperature and humidity sensor """

  def __init__(self, i2c_addr=0x40, dbhost="localhost", dbport=8086, dbname=None):

    self.i2c_addr = i2c_addr
    self.bus = smbus.SMBus(1)
    self.dbclient = influxdb.InfluxDBClient(dbhost, dbport, database=dbname)

  def execute(self):

    # Query for relative humidity
    self.bus.write_byte(self.i2c_addr, 0xF5)
    time.sleep(0.3)

    # Read the two byes back
    data0 = self.bus.read_byte(self.i2c_addr)
    data1 = self.bus.read_byte(self.i2c_addr)

    # Convert the data
    humidity = ((data0 * 256 + data1)  * 125 / 65536.0) - 6

    time.sleep(0.3)

    # Select temperature NO HOLD master mode
    self.bus.write_byte(self.i2c_addr, 0xF3)
    time.sleep(0.3)

    # Read data back
    data0 = self.bus.read_byte(self.i2c_addr)
    data1 = self.bus.read_byte(self.i2c_addr)

    # Convert data
    temp_c = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
    temp_f = temp_c * 9/5 + 32

    point = {"measurement": "SI7201 Temp+Humidity", "fields": {
      "humidity": humidity,
      "temp_c": temp_c,
      "temp_f": temp_f
    }}

    self.dbclient.write_points([point])
