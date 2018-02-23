import logging
import logging.handlers
import argparse
import os
import time

import influxdb

from animation import Gif_Playlist
from controller import LEDMatrix_Controller
from games import Game_Snake
from pattern import Pattern_Fire, Pattern_Munch, Pattern_Sine
from data.mappers.current_obs import Current_Obs_Mapper
from data.mappers.sunrise_sunset import Sunrise_Mapper
from data.mappers.indoor_temp import Indoor_Mapper
from components.indicator import Indicator
from gif_icons import Gif_Icon

current_dir = os.path.dirname(os.path.abspath(__file__))
GENGIFS_FOLDER = os.path.normpath(os.path.join(current_dir, "../icons/gifs/"))
GIFICON_FOLDER = os.path.normpath(os.path.join(current_dir, "../icons/gif_icons/"))

INFLUX_HOST = "ledmatrix"
INFLUX_DB = "home"

LOG_FILENAME = "log/ledmatrix.log"

# Set up logging
current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.normpath(os.path.join(current_dir, LOG_FILENAME))
log = logging.getLogger("ledmatrix")
log.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(
    log_path, maxBytes=1000000, backupCount=3)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s:%(lineno)d - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

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

  # FOR NEW GIFS ONLY
  import glob
  import os
  import random
  files = [name for name in glob.glob(os.path.join(
      GIFICON_FOLDER, '*.gif')) if os.path.isfile(os.path.join(GIFICON_FOLDER, name))]

  random.shuffle(files)

  #for filename in files:
  #  controller.items.append(os.path.basename(filename), Gif_Icon(dev, filename, timeout_ms=10000))

  #controller.items.append("Icons", Gif_Icon(dev, GIFICON_FOLDER + "/1629_icon_thumb.gif"))
  
  current_obs = Current_Obs_Mapper("KLGA")
  controller.items.append("Current Conditions",
                          Indicator(dev, current_obs))

  sunrise = Sunrise_Mapper(40.7127837,  -74.0059413)
  controller.items.append("Sunrise", Indicator(dev, sunrise))
  
  # indoor = Indoor_Mapper()
  # controller.items.append("Indoor", Indicator(dev, indoor))
  
  controller.items.append("Snake", Game_Snake(dev))
  
  # controller.items.append("Munch", Pattern_Munch(dev))
  # controller.items.append("Fire", Pattern_Fire(dev))
  #
  controller.items.append("GIF", Gif_Playlist(
      dev, GENGIFS_FOLDER, timeout_ms=10000))

  ui.mainloop()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass
