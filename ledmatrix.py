from rgbmatrix import Adafruit_RGBmatrix
from still_image import Still_Image

if __name__ == "__main__":
  matrix = Adafruit_RGBmatrix(32, 1)

  filename = "/home/pi/github/ledmatrix/icons/casinoicons/Cherry_32x32-32.png"

  cherry = Still_Image(filename, matrix)

  cherry.display()
