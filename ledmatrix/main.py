# Main file for ledmatrix
import time

import lirc

if __name__ == "__main__":

  # Initialize the remote control
  remote_controller = lirc.init("ledmatrix", "lircrc", blocking=False)

  while True:
    print "listening..."
    print lirc.nextcode()
    time.sleep(0.50)
