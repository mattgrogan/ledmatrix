class Viewport_Mixin(object):
  """
  Mixin to help move around the image
  """

  def reset(self):
    """ Reset the viewport """

    self._position = (0, 0)

  def set_position(self, xy):

    self._position = xy

  def move_left(self):

    x, y = self._position
    self.set_position((x + 1, y))

  def crop(self, wh):
    """ Crop at width and height """

    w, h = wh

    (left, top) = self._position
    right = left + w
    bottom = top + h

    im = self.image.crop(box=(left, top, right, bottom))
    im.load()  # Force the crop
    return im

  @property
  def is_finished(self):

    x, y = self._position
    return x >= self.image.size[0]
