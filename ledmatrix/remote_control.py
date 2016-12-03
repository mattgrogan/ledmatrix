
LIRCRC_CONFIG_FILE = "./lircrc"


class Remote_Control(object):
  """ Configure LIRC to receive remote control """

  def __init__(self, blocking=False):
    """ Initialize the remote control """

    import lirc

    self.rc = lirc.init("ledmatrix", LIRCRC_CONFIG_FILE, blocking=blocking)

    # These are all the possible events that can be sent by lirc. They
    # are configured in the lirc configuration file.
    self._event_names = [u"KEY_RIGHT", u"KEY_LEFT",
                         u"KEY_UP", u"KEY_DOWN",
                         u"KEY_STOP"]
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
    """ Read a command from the remote """

    import lirc
    code = lirc.nextcode()

    if len(code) > 0:
      print code

    if len(code) > 0 and code[0] in self._event_names:
      print "Found %s" % code[0]
      self.notify(code[0])
      return True
    else:
      return False


class Mock_Remote_Control(object):

  def read_command(self):
    pass
