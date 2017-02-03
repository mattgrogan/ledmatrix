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

  def display(self, image):

    raise NotImplementedError()

  def clear(self):

    self.display(Image.new(self.mode, self.size))


class RGB_Matrix(Device):
  """
  Handles output to the Adafruit RGB Matrix
  """

  def __init__(self):

    self.capabilities(MATRIX_WIDTH, MATRIX_HEIGHT, mode="RGB")

    # Use Adafruit's RGB Matrix class
    from rgbmatrix import Adafruit_RGBmatrix
    self._matrix = Adafruit_RGBmatrix(32, 1)

  def display(self, image):

    self._matrix.SetImage(image.im.id)

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

  def display(self, image):

    import PIL.ImageTk as ImageTk

    w = self.width * self._zoom
    h = self.height * self._zoom

    image = image.resize((w, h))
    image = ImageTk.PhotoImage(image)

    self._label.image = image
    self._label.configure(image=image)

Tk_Image.set_image = Tk_Image.display
