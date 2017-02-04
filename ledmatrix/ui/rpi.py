from __future__ import division

import sys
import time

from gpiozero import Button

BUTTON_GPIO_PIN = 24
TICK_MS = 10.0


class Rpi_UI(object):

  def __init__(self, controller):

    self.controller = controller

    # Set up the matrix
    from device import RGB_Matrix
    self.matrix = RGB_Matrix()

    # Handle control messages
    from zmq_control import ZeroMQ_Control
    self.zmq = ZeroMQ_Control()

    self.zmq.register("KEY_PLAYPAUSE", controller, controller.handle_playpause)
    self.zmq.register("KEY_STOP", controller, controller.handle_mode)
    self.zmq.register("KEY_UP", controller, controller.handle_up)
    self.zmq.register("KEY_DOWN", controller, controller.handle_down)
    self.zmq.register("KEY_LEFT", controller, controller.handle_left)
    self.zmq.register("KEY_RIGHT", controller, controller.handle_right)

    # Handle the physical button
    self.button = Button(BUTTON_GPIO_PIN)
    self.button.when_released = self.controller.handle_mode

  def mainloop(self):

    while True:
      # Have we received any zmq messages?
      self.zmq.read_command()

      # Run this iteration
      requested_delay_ms = self.controller.run()

      # Round up to the tick
      requested_delay_ms = max(requested_delay_ms, TICK_MS)

      # Hold in small increments until we've reached requested_delay_ms
      current_delay_ms = 0
      while current_delay_ms < requested_delay_ms:
        time.sleep(TICK_MS / 1000.0)
        current_delay_ms += TICK_MS
