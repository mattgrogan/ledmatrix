import logging
import sys
import time

log = logging.getLogger("ledmatrix")


class Sensor_Controller(object):

  def __init__(self):

    self.sensors = []

  def add_sensor(self, sensor):

    self.sensors.append(sensor)

  def mainloop(self):
    """ Run the execute method on each sensor """

    while True:

      for sensor in self.sensors:
        try:
          sensor.execute()
        except KeyboardInterrupt:
          sys.exit("Exiting...")
        except Exception as e:
          log.exception("Exception")

        time.sleep(0.01)
