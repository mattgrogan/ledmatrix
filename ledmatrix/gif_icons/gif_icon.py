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

  def __init__(self, device, filename, timeout_ms=None):
    self.device = device
    self.filename = filename
    self.timeout_ms = timeout_ms
    self.time_played_ms = 0
    self.eof = False

    self.current_frame = 0
    self.frames = []
    self.durations = []

    im = Image.open(self.filename)

    for frame in ImageSequence.Iterator(im):

        # Initialize a new image
        new_image = Image.new("RGB", (width, height), "black")
        new_pix = new_image.load()

        # Load the frame from the gif
        gif_image = frame.convert("RGB")
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

  @property
  def is_finished(self):
    """ We're finished if we're at the eof and we've passed the timeout """

    if self.timeout_ms is None:
      is_finished = self.eof
    elif self.eof and self.time_played_ms >= self.timeout_ms:
      is_finished = True
    else:
      is_finished = False

    return is_finished

  def start(self, timeout_ms=None):
    """ Reset to the beginning """

    #self.timeout_ms = timeout_ms
    self.time_played_ms = 0
    self.eof = False
    self.current_frame = 0

  def draw_frame(self):

    if self.current_frame >= len(self.frames):
      self.current_frame = 0

    self.device.clear()
    self.device.image.paste(self.frames[self.current_frame], (0,0))
    frame_duration_ms = self.durations[self.current_frame]

    self.current_frame += 1

    if self.current_frame >= len(self.frames):
      self.eof = True

    self.time_played_ms += frame_duration_ms

    self.device.display()

    return frame_duration_ms
