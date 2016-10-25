from gif_image import Gif_Image
from rgbmatrix import Adafruit_RGBmatrix
from still_image import Still_Image
from text import Text
from wander_image import Wander_Image

if __name__ == "__main__":
  matrix = Adafruit_RGBmatrix(32, 1)

  #filename = "/home/pi/github/ledmatrix/icons/gifs/ufo.gif"

  #cherry = Gif_Image(filename, matrix)

  #filename = "/home/pi/github/rpi-rgb-led-matrix/img/mattmike.jpg"

  # cherry.display(30)
  # utext = u"\uf080 \uf080 \uf080 \uf080 \uf080 \uf188 \uf219" # for
  # fontawsome
  #text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
  #t = Text(matrix)
  # t.display_scroll(text)

  #w = Wander_Image(filename, matrix)
  # w.display()

  filename = "/home/pi/github/ledmatrix/ovc.png"
  i = Still_Image(filename, matrix)
  i.display()
