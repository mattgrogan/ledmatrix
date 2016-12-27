import Adafruit_BMP.BMP280 as BMP280
import influxdb


class Temperature_Sensor_BMP280(object):

  def __init__(self, i2c_addr=0x76, dbhost="localhost", dbport=8086, dbname=None):

    self.sensor = BMP280.BMP280(address=i2c_addr)
    self.dbclient = influxdb.InfluxDBClient(dbhost, dbport, database=dbname)

  def execute(self):

    # Read temperature
    temp_c = self.sensor.read_temperature()
    temp_f = temp_c * 9 / 5 + 32

    point = {"measurement": "temp", "fields": {"value": temp_f}}

    self.dbclient.write_points([point])

    # Read pressure
    pa = self.sensor.read_pressure()

    point = {"measurement": "pressure", "fields": {"value": pa}}

    self.dbclient.write_points([point])
