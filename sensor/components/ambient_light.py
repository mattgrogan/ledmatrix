import Adafruit_VCNL40xx
import influxdb


class Ambient_Light_Sensor(object):

  def __init__(self, i2c_addr=0x76, dbhost="localhost", dbport=8086, dbname=None):

    self.vcnl = Adafruit_VCNL40xx.VCNL4010()
    self.dbclient = influxdb.InfluxDBClient(dbhost, dbport, database=dbname)

  def execute(self):

    proximity = self.vcnl.read_proximity()
    ambient = self.vcnl.read_ambient()

    prox_point = {"measurement": "proximity", "fields": {"value": proximity}}
    amb_point = {"measurement": "ambient_light", "fields": {"value": ambient}}

    self.dbclient.write_points([prox_point, amb_point])
