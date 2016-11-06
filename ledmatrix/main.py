import argparse
import os
import time

from animation import Gif_Playlist
from info import Clock
from main_controller import Main_Controller

current_dir = os.path.dirname(os.path.abspath(__file__))
GENGIFS_FOLDER = os.path.normpath(os.path.join(current_dir, "../icons/gifs/"))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="LED Matrix Animation")
  parser.add_argument("-output", required=False, choices=[
                      "gui", "rpi"], default="rpi")

  args = parser.parse_args()

  controller = Main_Controller()

  controller.add_menu_item(Clock(32, 32))
  controller.add_menu_item(Gif_Playlist(GENGIFS_FOLDER, timeout_ms=10000))

  # Running on the Raspberry Pi
  if args.output == "rpi":
    from ui.rpi import Rpi_UI
    ui = Rpi_UI(controller)
  elif args.output == "gui":
    from ui.gui import Gui
    ui = Gui(controller)

  ui.mainloop()
