from PIL import Image, ImageDraw
from components import Font_Mixin, Viewport_Mixin

class Text(Font_Mixin, Viewport_Mixin):
  """ Write text to an image """

  def __init__(self, text):

    self.text = text
    w, h = self.small_font.getsize(text)

    # Create the blank image for this frame
    self.image = Image.new("RGB", (w, h))

    # Add the text
    draw = ImageDraw.Draw(self.image)
    draw.text((0, 0), self.text, font=self.small_font)

    self.reset()

  @property
  def size(self):

    return self.image.size
