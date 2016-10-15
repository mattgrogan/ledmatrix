import time

import lirc
from gif_player import Gif_Player
from gif_playlist import Gif_Playlist
from rgbmatrix import Adafruit_RGBmatrix


class Main_Controller(object):
  """ This is the main controller for the LED Matrix """

  def __init__(self):
    """ Initialize the controller """

    self.matrix = Adafruit_RGBmatrix(32, 1)

    # Initialize the remote control
    self.remote_controller = lirc.init(
        "ledmatrix", "./lircrc", blocking=False)

  def run(self):
    """ Run the animations """

    folder = "/home/pi/github/ledmatrix/icons/gifs"

    gif_player = Gif_Playlist(folder, self.matrix)

    while True:

      delay, eof = gif_player.draw_frame()

      time.sleep(delay)

      code = lirc.nextcode()

      if len(code) > 0 and code[0] == u"KEY_RIGHT":
        gif_player.move(1)
      elif len(code) > 0 and code[0] == u"KEY_LEFT":
        gif_player.move(-1)
