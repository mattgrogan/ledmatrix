
import time
import Adafruit_BMP.BMP280 as BMP280
import influxdb

BMP280_ADDRESS = 0x76

# Data for influxdb
DBHOST = "ledmatrix"
DBPORT = 8086
DBNAME = "home"

sensor = BMP280.BMP280(address=BMP280_ADDRESS)
client = influxdb.InfluxDBClient(DBHOST, DBPORT, database=DBNAME)

while True:
  temp_f = sensor.read_temperature() * 9/5 + 32
  point = { "measurement": "temp", 
            "fields": { "value": temp_f }
          }
  client.write_points([point])
  #client.write(point)

  print 'Temp = {0:0.2f} *F'.format(sensor.read_temperature()*9/5+32)

  time.sleep(1)

