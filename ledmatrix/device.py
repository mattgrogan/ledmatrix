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


class Viewport(Device):
  """
  Virtual device which can handle any size image
  """

  def __init__(self, device, width, height, image=None):

    self.capabilities(width, height, device.mode)
    self._device = device
    self._position = (0, 0)

    if image is not None:
      self.image = image.resize((width, height), Image.ANTIALIAS)
      assert self.image.mode == self._device.mode

  def set_position(self, xy):
    self._position = xy
    self.display()

  def display(self):

    im = self.image.crop(box=self._crop_box())
    self._device.image = im
    self._device.display()
    del im

  def _crop_box(self):

    (left, top) = self._position
    right = left + self._device.width
    bottom = top + self._device.height

    assert(0 <= left <= right <= self.width)
    assert(0 <= top <= bottom <= self.height)

    return (left, top, right, bottom)


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

    del im
