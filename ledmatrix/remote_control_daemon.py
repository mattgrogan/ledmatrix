import zmq

import lirc

LIRCRC_CONFIG_FILE = "./lircrc"

if __name__ == "__main__":

  rc = lirc.init("ledmatrix", LIRCRC_CONFIG_FILE)

  # These are all the possible events that can be sent by lirc. They
  # are configured in the lirc configuration file.
  event_names = ["KEY_RIGHT", "KEY_LEFT",
                 "KEY_UP", "KEY_DOWN",
                 "KEY_STOP"]

  context = zmq.Context()
  socket = context.socket(zmq.PUSH)
  socket.connect("tcp://localhost:%s" % 5555)

  while True:
    code = lirc.nextcode()

    if len(code) > 0:
      print code

    if len(code) > 0 and code[0] in event_names:
      print "Found %s" % code[0]
      socket.send(str(code[0]))
