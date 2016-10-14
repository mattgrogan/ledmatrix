import time

import lirc
from gif_player import Gif_Player
from rgbmatrix import Adafruit_RGBmatrix


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self):
    """ Initialize the controller """

    self.matrix = Adafruit_RGBmatrix(32, 1)

    # Initialize the remote control
    self.remote_controller = lirc.init("ledmatrix", "lircrc", blocking=False)

  def run(self):
    """ Run the animations """

    filename = "/home/pi/github/ledmatrix/icons/gifs/ufo.gif"

    gif_player = Gif_Player(filename, self.matrix)

    while True:

      delay, eof = gif_player.draw_frame()

      if eof:
        print "EOF"

      time.sleep(delay)
