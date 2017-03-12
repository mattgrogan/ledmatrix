import argparse
import os
import time

from animation import Gif_Playlist, Photo_Image
from controller import LEDMatrix_Controller
from games import Game_Snake
from info import Clock, Countdown, Messages
from pattern import Pattern_Fire, Pattern_Munch, Pattern_Sine

current_dir = os.path.dirname(os.path.abspath(__file__))
GENGIFS_FOLDER = os.path.normpath(os.path.join(current_dir, "../icons/gifs/"))


def main():

  parser = argparse.ArgumentParser(description="LED Matrix Animation")
  parser.add_argument("-output", required=False, choices=[
                      "gui", "rpi"], default="rpi")

  args = parser.parse_args()

  controller = LEDMatrix_Controller()

  if args.output == "rpi":
    from ui.rpi import Rpi_UI
    ui = Rpi_UI(controller)
  elif args.output == "gui":
    from ui.gui import Gui
    ui = Gui(controller)

  dev = ui.matrix

  #controller.items.append("Image", Photo_Image(dev))

  controller.items.append("Messages", Messages(dev, station="KLGA"))

  controller.items.append("Clock", Clock(dev, station="KLGA"))

  controller.items.append("Snake", Game_Snake(dev))

  controller.items.append("Munch", Pattern_Munch(dev))
  controller.items.append("Fire", Pattern_Fire(dev))
  controller.items.append("GIF", Gif_Playlist(
      dev, GENGIFS_FOLDER, timeout_ms=10000))

  controller.items.append("Countdown", Countdown(dev))

  ui.mainloop()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass
