import logging
import os
import time

import zmq

import lirc

log = logging.getLogger("ledmatrix")

current_dir = os.path.dirname(os.path.abspath(__file__))
LIRC_CONFIG_FILE = os.path.normpath(os.path.join(current_dir, "lircrc"))


class IR_Remote(object):
  """ Read commands from infrared sensor and forward to zmq on ledmatrx """

  def __init__(self, host="localhost", port=5555):

    self.host = host
    self.port = port
    self.addr = "tcp://%s:%s" % (self.host, self.port)

    # Events that can be read from lirc configuration file
    self.events = ["KEY_RIGHT", "KEY_LEFT", "KEY_UP", "KEY_DOWN",
                   "KEY_STOP", "KEY_ENTER", "KEY_PLAYPAUSE"]

    self.zmq_context = zmq.Context()
    self.socket = self.zmq_context.socket(zmq.PUSH)
    self.socket.connect(self.addr)

    # Initialize lirc
    lirc.init("ledmatrix", LIRC_CONFIG_FILE, blocking=False)

    log.info("Initialized IR Remote")

  def read_ir_code(self):

    code = lirc.nextcode()

    if len(code) > 0 and code[0] in self.events:
      return_code = str(code[0])
    else:
      return_code = None

    return return_code

  def execute(self):
    """ Read and forward to zmq """

    code = self.read_ir_code()

    if code is not None:

      log.info("Received: %s " % code)

      try:
        self.socket.connect(self.addr)
        self.socket.send(code)
      except zmq.ZMQError:
        log.critical("Unable to connect to %s" % self.addr)
      finally:
        pass
        # self.socket.close()


if __name__ == "__main__":

  remote = IR_Remote(host="ledmatrix")

  while True:
    remote.execute()
    time.sleep(0.1)
