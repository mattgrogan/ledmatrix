from PIL import Image, ImageChops, ImageDraw, ImageFont

SMALLFONT = "/home/pi/github/ledmatrix/fonts/small_pixel.ttf"
SMALLFONTSIZE = 8


class Message_Player(object):
  """ Display a message scrolling across the screen """

  def __init__(self, matrix, width, height):
    """ Initialize the display """

    self.matrix = matrix
    self.width = width
    self.height = height

    self.small_font = ImageFont.truetype(SMALLFONT, SMALLFONTSIZE)

    self.message = None
    self.image = None
    self.draw = None
    self.image_width = None

    self.xoffset = None

  def start(self, message, color=0xFFFFFF):
    """ Set up the message """

    self.message = message

    w, h = self.small_font.getsize(message)

    # Imagewidth is the text width plus a blank screen
    self.image_width = w + self.width

    self.image = Image.new('RGB', (self.image_width, self.height))
    self.draw = ImageDraw.Draw(self.image)

    yloc = (self.height - h) / 2

    self.draw.text((0, yloc), message, font=self.small_font, fill=color)

    self.xoffset = 0

  def move(self, step=1):
    """ Reset """

    self.start(self.message)

  def draw_frame(self):
    """ Subset the image and draw the frame """

    offset_image = ImageChops.offset(self.image, -1 * self.xoffset, 0)
    cropped_image = offset_image.crop((0, 0, self.width - 1, self.height - 1))

    self.matrix.SetImage(cropped_image.im.id)

    self.xoffset += 1

    if self.xoffset >= self.image_width:
      self.xoffset = 0

    return 0.075
