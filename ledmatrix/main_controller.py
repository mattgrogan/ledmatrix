import time

import lirc


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self):
    """ Initialize the controller """

    # Initialize the remote control
    remote_controller = lirc.init("ledmatrix", "lircrc", blocking=False)

  def run(self):
    """ Run the animations """

    while True:
      print "listening..."
      print lirc.nextcode()
      time.sleep(0.50)
