import argparse
import time

from gif_playlist import Gif_Playlist
from main_controller import Main_Controller
from time_player import Time_Player

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="LED Matrix Animation")
  parser.add_argument("-output", required=False, choices=[
                      "gui", "rpi"], default="rpi")

  args = parser.parse_args()

  if args.output == "rpi":
    # Running on the Raspberry Pi

    from matrix_adapter import Adafruit_Matrix_Adapter
    matrix = Adafruit_Matrix_Adapter()
    controller = Main_Controller(matrix)

    import lirc
    from remote_control import Remote_Control

    rc = Remote_Control()
    rc.register(u"KEY_STOP", controller, controller.handle_stop)
    rc.register(u"KEY_UP", controller, controller.handle_up)
    rc.register(u"KEY_DOWN", controller, controller.handle_down)
    rc.register(u"KEY_LEFT", controller, controller.handle_left)
    rc.register(u"KEY_RIGHT", controller, controller.handle_right)

    controller.add_menu_item(Time_Player(32, 32))

    gengifs_folder = "/home/pi/github/ledmatrix/icons/gifs"
    controller.add_menu_item(Gif_Playlist(gengifs_folder))

    halogifs_folder = "/home/pi/github/ledmatrix/icons/halogifs"
    controller.add_menu_item(Gif_Playlist(halogifs_folder))

    while True:
      delay = controller.run(rc)
      time.sleep(delay)

  elif args.output == "gui":
    import Tkinter as tk
    from gui import LED_Gui

    controller = Main_Controller()

    controller.add_menu_item(Time_Player(32, 32))

    gengifs_folder = "x:/github/ledmatrix/icons/gifs"
    controller.add_menu_item(Gif_Playlist(gengifs_folder))

    from remote_control import Mock_Remote_Control
    rc = Mock_Remote_Control()

    root = tk.Tk()
    app = LED_Gui(root, controller, rc)
    controller.matrix = app
    root.after(0, app.start)

    root.mainloop()
