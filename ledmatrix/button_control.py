import zmq

from button import Button

GPIO_PIN = 24


class Button_Control(object):
  """ Configure button to act as remote control """

  def __init__(self, blocking=False):

    # The button
    self.button = Button("Mode", GPIO_PIN)
    self.button.enabled = True

    # The zmq
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.PUSH)
    self.socket.connect("tcp://localhost:%s" % 5555)

    self._event_names = ["KEY_STOP"]
    self._events = None
    self._events = {event: dict() for event in self._event_names}

  def register(self, event, who, callback=None):

    if callback is None:
      callback = getattr(who, 'update')

    try:
      self._events[event][who] = callback
    except KeyError:
      print "Key %s not supported in Button_Control" % event

  def notify(self, event, message=None):

    for subscriber, callback in self._events[event].iteritems():
      callback(message)

  def read_command(self):

    if self.button.event_detected:
      code = self._event_names[0]
      self.socket.send(code)
