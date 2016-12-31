import logging
import logging.handlers
import os
import sys

from components.ir_remote import IR_Remote
from components.si7201 import SI7201
from sensor_controller import Sensor_Controller

ZMQ_HOST = "ledmatrix"
INFLUX_HOST = "ledmatrix"
INFLUX_DB = "home"
LOG_FILENAME = "sensor.log"

# Set up logging
current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.normpath(os.path.join(current_dir, LOG_FILENAME))

log = logging.getLogger("ledmatrix")
log.setLevel(logging.INFO)


handler = logging.handlers.RotatingFileHandler(
    log_path, maxBytes=1000000, backupCount=3)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s:%(lineno)d - %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

if __name__ == "__main__":

  log.info("Starting sensor readings")

  controller = Sensor_Controller()

  ir_remote = IR_Remote(host=ZMQ_HOST)
  temp_humidity = SI7201(dbhost=INFLUX_HOST, dbname=INFLUX_DB)

  controller.add_sensor(ir_remote)
  controller.add_sensor(temp_humidity)

  controller.mainloop()
