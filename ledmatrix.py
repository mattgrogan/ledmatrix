from gif_image import Gif_Image
from rgbmatrix import Adafruit_RGBmatrix
from still_image import Still_Image

if __name__ == "__main__":
  matrix = Adafruit_RGBmatrix(32, 1)

  filename = "/home/pi/github/ledmatrix/icons/gifs/ufo.gif"

  cherry = Gif_Image(filename, matrix)

  cherry.display(30)
