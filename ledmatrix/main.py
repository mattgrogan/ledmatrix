import argparse

from gif_playlist import Gif_Playlist
from main_controller import Main_Controller
from message_player import Message_Player
from rgbmatrix import Adafruit_RGBmatrix
from time_player import Time_Player
from weather_playlist import Weather_Playlist

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="LED Matrix Animation")
  parser.add_argument("-output", required=False, choices=[
                      "gui", "led"], default="led")

  args = parser.parse_args()

  if args.output == "led":
    matrix = Adafruit_RGBmatrix(32, 1)

    import lirc
    from remote_control import Remote_Control

    controller = Main_Controller(matrix)

    rc = Remote_Control()
    rc.register(u"KEY_STOP", controller, controller.handle_stop)
    rc.register(u"KEY_UP", controller, controller.handle_up)
    rc.register(u"KEY_DOWN", controller, controller.handle_down)
    rc.register(u"KEY_LEFT", controller, controller.handle_left)
    rc.register(u"KEY_RIGHT", controller, controller.handle_right)

  #wp = Weather_Playlist(matrix, 32, 32)
  # wp.update_weather()
  # controller.add_menu_item(wp)

  controller.add_menu_item(Time_Player(32, 32))

  gengifs_folder = "/home/pi/github/ledmatrix/icons/gifs"
  controller.add_menu_item(Gif_Playlist(gengifs_folder))

  halogifs_folder = "/home/pi/github/ledmatrix/icons/halogifs"
  controller.add_menu_item(Gif_Playlist(halogifs_folder))

  controller.run(rc)
