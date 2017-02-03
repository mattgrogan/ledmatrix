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

  controller.add_menu_item(Clock(MATRIX_WIDTH, MATRIX_HEIGHT))

  controller.add_menu_item(Countdown(MATRIX_WIDTH, MATRIX_HEIGHT))

  controller.add_menu_item(Pattern_Sine(MATRIX_WIDTH, MATRIX_HEIGHT))
  controller.add_menu_item(Gif_Playlist(XMAS_FOLDER, timeout_ms=10000))
  controller.add_menu_item(Gif_Playlist(GENGIFS_FOLDER, timeout_ms=10000))
  controller.add_menu_item(Pattern_Munch(MATRIX_WIDTH, MATRIX_HEIGHT))
  controller.add_menu_item(Game_Snake(MATRIX_WIDTH, MATRIX_HEIGHT))
  controller.add_menu_item(Pattern_Fire(MATRIX_WIDTH, MATRIX_HEIGHT))

  # Running on the Raspberry Pi
  if args.output == "rpi":
    from ui.rpi import Rpi_UI
    ui = Rpi_UI(controller)
  elif args.output == "gui":
    from ui.gui import Gui
    ui = Gui(controller)

  ui.mainloop()
