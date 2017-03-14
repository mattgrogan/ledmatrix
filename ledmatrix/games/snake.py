import random
import time
from canvas import canvas
from collections import deque
from PIL import ImageColor

from components import App


class Game_Snake(App):

  def __init__(self, device):

    self.device = device

    self.width = device.width
    self.height = device.height

    self.direction = "RIGHT"
    self.snakehead = None
    self.apple = (None, None)
    self.segments = deque()
    self.segment_count = None
    self.max_segment_count = 1024
    self.movespeed = 150

    self.is_setup = False

    self.snake_color = ImageColor.getrgb("#FFFDB7")
    self.apple_color = ImageColor.getrgb("#1BA363")
    self.black_color = (0, 0, 0)

  def new_apple(self):

    while True:
      # Find a random place
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - 1)

      # Check that there's no overlap
      if not (x, y) in self.segments:
        self.apple = (x, y)
        break

  def handle_input(self, command):

    if command == "UP":
      if self.direction != "DOWN":
        self.direction = "UP"
    elif command == "DOWN":
      if self.direction != "UP":
        self.direction = "DOWN"
    elif command == "LEFT":
      if self.direction != "RIGHT":
        self.direction = "LEFT"
    elif command == "RIGHT":
      if self.direction != "LEFT":
        self.direction = "RIGHT"

  def update(self):

    x, y = self.snakehead

    if self.direction == "UP":
      y -= 1
    elif self.direction == "DOWN":
      y += 1
    elif self.direction == "LEFT":
      x -= 1
    elif self.direction == "RIGHT":
      x += 1

    # Wrap around
    if x >= self.width:
      x = 0
    elif x < 0:
      x = self.width - 1

    if y >= self.height:
      y = 0
    elif y < 0:
      y = self.height - 1

    if (x, y) in self.segments:
      self.die()

    self.segments.appendleft((x, y))

    if (x, y) == self.apple:
      self.segment_count += 1

      if self.segment_count > self.max_segment_count:
        self.segment_count = self.max_segment_count

      self.new_apple()

    # Trim the end of the snake
    while (len(self.segments) > self.segment_count):
      p = self.segments.pop()

    self.snakehead = (x, y)

  def die(self):
    time.sleep(1)
    self.setup()

  def setup(self):

    self.new_apple()
    self.snakehead = (self.width / 2, self.height / 2)
    self.direction = "RIGHT"
    self.is_setup = True
    self.segments = deque()
    self.segment_count = 4

  def draw_frame(self):

    if not self.is_setup:
      self.setup()

    self.update()

    with canvas(self.device) as draw:

      draw.point(self.apple, self.apple_color)

      for point in list(self.segments):
        draw.point(point, self.snake_color)

    return self.movespeed
