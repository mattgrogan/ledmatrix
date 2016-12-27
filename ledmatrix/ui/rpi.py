from __future__ import division, print_function

import sys
import time

TICK_MS = 25.0


class Rpi_UI(object):

  def __init__(self, controller):

    self.controller = controller

    from matrix_adapter import Adafruit_Matrix_Adapter
    self.controller.matrix = Adafruit_Matrix_Adapter()

    #from remote_control import Remote_Control
    #self.rc = Remote_Control()

    from zmq_control import ZeroMQ_Control
    self.rc = ZeroMQ_Control()
    from button_control import Button_Control
    self.rc2 = Button_Control()

    self.rc.register("KEY_PLAYPAUSE", controller, controller.handle_playpause)
    self.rc.register("KEY_STOP", controller, controller.handle_mode)
    self.rc.register("KEY_UP", controller, controller.handle_up)
    self.rc.register("KEY_DOWN", controller, controller.handle_down)
    self.rc.register("KEY_LEFT", controller, controller.handle_left)
    self.rc.register("KEY_RIGHT", controller, controller.handle_right)

  def mainloop(self):

    while True:
      # rc2 is a hack for now. Can't get lirc to work.
      self.rc2.read_command(self.controller.is_running)
      self.rc.read_command()

      requested_delay_ms = self.controller.run()

      if requested_delay_ms < TICK_MS:
        requested_delay_ms = TICK_MS
      time.sleep(requested_delay_ms / 1000.0)
