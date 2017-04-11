from PIL import Image, ImageDraw

from components import Font_Mixin, Viewport_Mixin, Viewport_NoScroll_Mixin


class Text(Font_Mixin, Viewport_Mixin):
  """ Write text to an image """

  def __init__(self, data_mapper, data_field=None, color="#FFFFFF", font="MEDIUM"):

    self.data_mapper = data_mapper
    self.data_field = data_field
    self.font = font
    self.color = color

    self.update()

    self.reset()

  def update(self):

    try:
      text = self.data_mapper[self.data_field]
    except:
      text = "NO DATA"

    w, h = self.font.getsize(text)

    # Create the blank image for this frame
    self.image = Image.new("RGB", (w, h))

    # Add the text
    draw = ImageDraw.Draw(self.image)
    draw.text((0, 0), text, font=self.font, fill=self.color)

  @property
  def size(self):

    return self.image.size


class NoScroll_Text(Text, Viewport_NoScroll_Mixin):
  pass
