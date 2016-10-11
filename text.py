import os
import textwrap
import time

from PIL import Image, ImageChops, ImageDraw, ImageFont

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32

dir = os.path.dirname(__file__)
#FONT_PATH = os.path.join(dir, '../fonts/VCR_OSD_MONO_1.001.ttf')
#FONT_PATH = os.path.join(dir, '../fonts/ARCADEPI.TTF')
# FONT_PATH = os.path.join(dir, 'fonts/Beefd.ttf') # size 5
FONT_SIZE = 8

FONT_PATH = os.path.join(dir, 'fonts/RPGSystem.ttf')  # size 8 looks goood


fontfile = "pixel_dingbats-7.ttf"  # 8px ** blah
fontfile = "V5_pixelpals.ttf"  # 20px *** faces
fontfile = "pixel_invaders.ttf"  # 18px ***** AMAZING
fontfile = "fontawesome-webfont.ttf"  # 14px, 16px,  ***** depends on character
fontfile = "meteocons.ttf"  # 16ok ** weather icons boring
fontfile = "acknowtt.ttf"  # 13px ***** nice 2px lines but kind of wide
fontfile = "Moder DOS 437.ttf"  # 16px Very nice, dark bold, 8px no good
fontfile = "Beefd.ttf"  # 5px good nice and small, kind of wide, too wide at 10
fontfile = "RPGSystem.ttf"  # 16px not wide, nice and big. not smaller\
fontfile = "ARCADEPI.TTF"  # 10px
fontfile = "small_pixel.ttf"  # 8px great small font

FONT_PATH = os.path.join(dir, 'fonts/' + fontfile)


class Text(object):
  """ This class prepares a gif image for display on the RGB Matrix """

  def __init__(self, matrix):
    """ Initialize with a reference to the RGB Matrix """

    #self.filename = filename
    self.matrix = matrix

    self.image = Image.new('RGB', (MATRIX_WIDTH, MATRIX_HEIGHT))
    self.draw = ImageDraw.Draw(self.image)

    # TODO: wrap in try statement
    #self.image = Image.open(filename)
    # self.image.load()

    # Resize if necessary
    # if self.image.size != (MATRIX_WIDTH, MATRIX_HEIGHT):
    #  self.image = self.image.resize(
    #      (MATRIX_WIDTH, MATRIX_HEIGHT), Image.ANTIALIAS)

    # Make sure it's RGB
    #self.image = self.image.convert("RGB")

  def display(self, text, duration=10):
    """ Display the text on the matrix for duration seconds. """

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    lines = textwrap.wrap(text, width=5)

    x = 0
    y = 0
    y_text = y

    for line in lines:
      width, height = font.getsize(line)
      self.draw.text((x, y_text), line, font=font, fill=255)
      y_text += height

    # Show the image
    self.matrix.SetImage(self.image.im.id)
    time.sleep(duration)

    self.matrix.Clear()

  def display_scroll(self, text, duration=10):
    """ Display the text as scrolling """

    MAX_WIDTH = 500

    image = Image.new('RGB', (MAX_WIDTH, MATRIX_HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    lines = textwrap.wrap(text, width=MAX_WIDTH / FONT_SIZE)

    x = 0
    y = 0
    y_text = y

    for line in lines:
      width, height = font.getsize(line)
      draw.text((x, y_text), line, font=font, fill=0xFFFFFF)
      y_text += height

    while True:

      for xoffset in range(MAX_WIDTH):

        offset_image = ImageChops.offset(image, -1 * xoffset, 0)

        cropped_image = offset_image.crop((0, 0, 31, 31))
        self.matrix.SetImage(cropped_image.im.id)
        time.sleep(0.05)
