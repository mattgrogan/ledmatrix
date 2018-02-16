from PIL import Image, ImageSequence
from components import App

width = 8
height = 8

X_OFFSET = 3
Y_OFFSET = 3

X_MULT = 5
Y_MULT = 5

class Gif_Icon(App):
  """ Shows an animated gif icon """

  def __init__(self, device, filename):
    self.device = device
    self.filename = filename

    self.current_frame = 0
    self.frames = []
    self.durations = []

    im = Image.open(self.filename)

    for frame in ImageSequence.Iterator(im):

        # Initialize a new image
        new_image = Image.new("RGBA", (width, height))
        new_pix = new_image.load()

        # Load the frame from the gif
        gif_image = frame.convert("RGBA")
        gif_pix = gif_image.load()

        # Find the encoded duration in milliseconds
        try:
          frame_duration_ms = frame.info["duration"]
        except KeyError:
          frame_duration_ms = 25

        self.durations.append(frame_duration_ms)

        # Map each pixel
        for col in range(width):
            x = col * X_MULT + X_OFFSET
            for row in range(height):
                y = row * Y_MULT + Y_OFFSET
                new_pix[col, row] = gif_pix[x, y]

        # Save the image
        self.frames.append(new_image)

  def draw_frame(self):

    if self.current_frame >= len(self.frames):
      self.current_frame = 0

    self.device.clear()
    self.device.image.paste(self.frames[self.current_frame], (0,0))

    self.current_frame += 1

    self.device.display()

    return self.durations[self.current_frame-1]
