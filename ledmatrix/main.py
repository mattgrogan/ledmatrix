import argparse
import os
import time

from animation import Gif_Playlist
from games import Game_Snake
from info import Clock, Countdown
from main_controller import Main_Controller
from pattern import Pattern_Fire, Pattern_Munch, Pattern_Sine

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32
current_dir = os.path.dirname(os.path.abspath(__file__))
GENGIFS_FOLDER = os.path.normpath(os.path.join(current_dir, "../icons/gifs/"))
XMAS_FOLDER = os.path.normpath(os.path.join(current_dir, "../icons/xmasgifs/"))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="LED Matrix Animation")
  parser.add_argument("-output", required=False, choices=[
                      "gui", "rpi"], default="rpi")

  args = parser.parse_args()

  controller = Main_Controller()

  # controller.add_menu_item(Pattern_Sine(MATRIX_WIDTH, MATRIX_HEIGHT))
  # controller.add_menu_item(Pattern_Munch(MATRIX_WIDTH, MATRIX_HEIGHT))

  # Running on the Raspberry Pi
  if args.output == "rpi":
    from ui.rpi import Rpi_UI
    ui = Rpi_UI(controller)
  elif args.output == "gui":
    from ui.gui import Gui
    ui = Gui(controller)

  dev = controller.matrix

  controller.items.append("Munch", Pattern_Munch(dev))
  controller.items.append("Fire", Pattern_Fire(dev))
  controller.items.append("GIF", Gif_Playlist(
      dev, GENGIFS_FOLDER, timeout_ms=10000))
  controller.items.append("Clock", Clock(dev, station="KLGA"))
  controller.items.append("Countdown", Countdown(dev))
  controller.items.append("Snake", Game_Snake(dev))

  ui.mainloop()
