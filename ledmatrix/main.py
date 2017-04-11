import argparse
import os
import time

import influxdb

from animation import Gif_Playlist
from apps import Weather_App, Indoor_App, Sun_App
from controller import LEDMatrix_Controller
from games import Game_Snake
from pattern import Pattern_Fire, Pattern_Munch, Pattern_Sine
from data.mappers.current_obs import Current_Obs_Mapper
from data.mappers.sunrise_sunset import Sunrise_Mapper
# from components.indicator_app import Indicator_App
from components.indicator import Indicator
# from components.indicator2 import Indicator2

current_dir = os.path.dirname(os.path.abspath(__file__))
GENGIFS_FOLDER = os.path.normpath(os.path.join(current_dir, "../icons/gifs/"))

INFLUX_HOST = "ledmatrix"
INFLUX_DB = "home"


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

  influx = influxdb.InfluxDBClient(
      INFLUX_HOST, 8086, database=INFLUX_DB, timeout=10)

  current_obs = Current_Obs_Mapper("KLGA")
  controller.items.append("Current Conditions",
                          Indicator(dev, current_obs))

  sunrise = Sunrise_Mapper(40.7127837,  -74.0059413)
  controller.items.append("Sunrise", Indicator(dev, sunrise))

  # controller.items.append("Indoor", Indoor_App(dev, influx))
  #
  # controller.items.append("Snake", Game_Snake(dev))
  #
  # controller.items.append("Munch", Pattern_Munch(dev))
  # controller.items.append("Fire", Pattern_Fire(dev))
  #
  # controller.items.append("GIF", Gif_Playlist(
  #     dev, GENGIFS_FOLDER, timeout_ms=10000))

  ui.mainloop()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass
