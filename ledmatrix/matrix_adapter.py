class Adafruit_Matrix_Adapter(object):

  def __init__(self):
    """ Use the Adafruit library to control the matrix """

    from rgbmatrix import Adafruit_RGBmatrix
    self.matrix = Adafruit_RGBmatrix(32, 1)

  def set_image(self, image):

    self.matrix.SetImage(image.im.id)

  def clear(self):

    self.matrix.Clear()
