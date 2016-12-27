import zmq

PORT = 5555


class ZeroMQ_Control(object):
  """ Receive messages from ZeroMQ """

  def __init__(self, port=PORT):

    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.PULL)
    self.socket.bind("tcp://*:%s" % port)
    #self.socket.setsockopt(zmq.SUBSCRIBE, "LEDMATRIX")

    self._event_names = [u"KEY_RIGHT", u"KEY_LEFT",
                         u"KEY_UP", u"KEY_DOWN",
                         u"KEY_STOP", u"KEY_PLAYPAUSE"]
    self._events = None
    self._events = {event: dict() for event in self._event_names}

  def register(self, event, who, callback=None):
    """ Register for ui events """

    if callback is None:
      callback = getattr(who, 'update')

    self._events[event][who] = callback

  def notify(self, event, message=None):
    """ Notify the subscribers for a particular event """

    for subscriber, callback in self._events[event].iteritems():
      callback(message)

  def read_command(self):

    events = self.socket.poll(timeout=1)

    if events:
      message = self.socket.recv()

      if message in self._event_names:
        self.notify(message)
        return True

    return False
