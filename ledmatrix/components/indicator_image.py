from PIL import Image, ImageEnhance


class Indicator_Image(object):
  """
  This object is responsible for composing an image given a list of
  components. As the image is animated, it will delegate the scrolling
  to each component.
  """

  def __init__(self, device):
    """
    The device is needed for its dimensions. The items will be cropped to
    fit within the screen.
    """

    self.device = device
    self._items = []
    self.brightness = 1.0

    # What's the bottom?
    self.y_loc = self.device.height - 1

  def add_item(self, item, xy):
    """
    Store the item and its location as a tuple
    """

    self._items.append((item, xy))

  def move_down(self):
    """
    Move the image down by one
    """

    w, h = self.image.size
    self.image = self.image.crop((0, self.y_loc, w - 1, h - 1))
    self.image.load()

    self.y_loc -= 1

    # Check have we scrolled all the way?
    if self.y_loc < 0:
      self.y_loc = h
      raise StopIteration

  def build_image(self):
    """
    Build an image and paste each item into its appropriate location
    """

    # Create the blank image for this frame
    self.image = Image.new(self.device.mode, self.device.size)

    for item, xy in self._items:
      item.update()
      im = item.crop(self.device.size)
      im.load()  # Force the crop
      self.image.paste(im, xy)

    # Set the brightness
    enhancer = ImageEnhance.Brightness(self.image)
    self.image = enhancer.enhance(self.brightness)

  def next(self):
    """
    Call move_left on each item in order to scroll the image. If all items
    are finished, then raise a StopIteration.
    """

    is_finished = True

    for item, xy in self._items:
      item.move_left()
      if not item.is_finished:
        is_finished = False  # If any item is not finished, we're not finished

    if is_finished:
      raise StopIteration

  def reset(self):
    """
    Reset the positions of each child item.
    """

    for item, xy in self._items:
      item.reset()
