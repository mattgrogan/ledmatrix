from PIL import Image, ImageDraw

from components import Font_Mixin, Viewport_Mixin, Viewport_NoScroll_Mixin


class Text(Font_Mixin, Viewport_Mixin):
  """ Write text to an image """

  def __init__(self, text, font="MEDIUM"):

    self.text = text
    self.font = font

    self.update()

    self.reset()

  def update(self):

    text = self.text()
    w, h = self.font.getsize(text)

    # Create the blank image for this frame
    self.image = Image.new("RGB", (w, h))

    # Add the text
    draw = ImageDraw.Draw(self.image)
    draw.text((0, 0), text, font=self.font)

  @property
  def size(self):

    return self.image.size


class NoScroll_Text(Text, Viewport_NoScroll_Mixin):
  pass
