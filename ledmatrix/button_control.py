import zmq

from state_button import State_Button

GPIO_PIN = 24


class Button_Control(object):
  """ Configure button to act as remote control """

  def __init__(self, blocking=False):

    # The button
    self.button = State_Button("Mode", GPIO_PIN)
    #self.button.enabled = True

    # The zmq
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.PUSH)
    self.socket.connect("tcp://localhost:%s" % 5555)

    self._event_names = ["KEY_STOP", "KEY_RIGHT", "KEY_PLAYPAUSE"]
    self._events = None
    self._events = {event: dict() for event in self._event_names}

  def read_command(self, is_running):

    code = None
    event = self.button.event_detected

    if event == "BUTTON_CLICK":
      code = "KEY_STOP"
    elif event == "BUTTON_PRESS":
      code = "KEY_RIGHT"
    elif event == "BUTTON_TIMEOUT":
      code = "KEY_PLAYPAUSE"

    if code is not None and not is_running:
      code = "KEY_PLAYPAUSE"

    if code is not None:
      self.socket.send(code)
