from PIL import Image

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32


class Device(object):

  def capabilities(self, width, height, mode):

    assert mode in ["1", "RGB", "RGBA"]

    self.height = width
    self.width = height
    self.size = (self.width, self.height)
    self.bounding_box = (0, 0, self.width - 1, self.height - 1)
    self.mode = mode

    self.image = Image.new(self.mode, self.size)

  def display(self, image):

    raise NotImplementedError()

  def clear(self):

    self.image = Image.new(self.mode, self.size)


class RGB_Matrix(Device):
  """
  Handles output to the Adafruit RGB Matrix
  """

  def __init__(self):

    self.capabilities(MATRIX_WIDTH, MATRIX_HEIGHT, mode="RGB")

    # Use Adafruit's RGB Matrix class
    from rgbmatrix import Adafruit_RGBmatrix
    self._matrix = Adafruit_RGBmatrix(32, 1)

  def display(self):

    self._matrix.SetImage(self.image.im.id)

  def clear(self):

    self._matrix.Clear()


class Tk_Image(Device):
  """
  Handles output to a TK PhotoImage

  This device is able to resize the original image to make it more
  legible on the screen. Note: remember to call self.update() on the
  tk object.

  :param tk.Label label:
    The Label to contain the image

  :param int zoom:
    Zoom level for the image

  """

  def __init__(self, label, zoom=1):

    self._label = label
    self._zoom = zoom

    self.capabilities(MATRIX_WIDTH, MATRIX_HEIGHT, mode="RGB")

  def display(self):

    import PIL.ImageTk as ImageTk

    w = self.width * self._zoom
    h = self.height * self._zoom

    im = self.image

    im = im.resize((w, h))
    im = ImageTk.PhotoImage(im)

    self._label.image = im
    self._label.configure(image=im)
