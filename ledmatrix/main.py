from gif_playlist import Gif_Playlist
from main_controller import Main_Controller
from null_player import Null_Player
from rgbmatrix import Adafruit_RGBmatrix
from time_player import Time_Player

if __name__ == "__main__":

  matrix = Adafruit_RGBmatrix(32, 1)

  controller = Main_Controller()
  controller.add_null_player(Null_Player(matrix))

  controller.add_menu_item(Time_Player(matrix, 32, 32))

  gengifs_folder = "/home/pi/github/ledmatrix/icons/gifs"
  controller.add_menu_item(Gif_Playlist(gengifs_folder, matrix))

  halogifs_folder = "/home/pi/github/ledmatrix/icons/halogifs"
  controller.add_menu_item(Gif_Playlist(halogifs_folder, matrix))

  controller.run()
