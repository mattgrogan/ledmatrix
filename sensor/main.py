
from components.ambient_light import Ambient_Light_Sensor
from components.ir_remote import IR_Remote
from components.temp import Temperature_Sensor_BMP280
from sensor_controller import Sensor_Controller

ZMQ_HOST = "ledmatrix"
INFLUX_HOST = "ledmatrix"
INFLUX_DB = "home"

if __name__ == "__main__":

  controller = Sensor_Controller()

  ir_remote = IR_Remote(host=ZMQ_HOST)
  temp_sensor = Temperature_Sensor_BMP280(dbhost=INFLUX_HOST, dbname=INFLUX_DB)
  ambient_light = Ambient_Light_Sensor(dbhost=INFLUX_HOST, dbname=INFLUX_DB)

  controller.add_sensor(ir_remote)
  controller.add_sensor(temp_sensor)
  controller.add_sensor(ambient_light)

  controller.mainloop()
