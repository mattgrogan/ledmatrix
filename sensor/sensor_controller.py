import sys
import time


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
        except Exception, e:
          logger.critical("Error", exec_info=True)

      time.sleep(0.1)
