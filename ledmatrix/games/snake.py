import copy
import random
import time
from collections import deque

import randomcolor
from PIL import Image, ImageColor


class Game_Snake(object):

  def __init__(self, width, height):

    self.width = width
    self.height = height

    self.direction = "RIGHT"
    self.snakehead = None
    self.apple = [None, None]
    self.segments = None
    self.segment_count = None
    self.max_segment_count = 1024
    self.movespeed = 150

    self.is_setup = False

    rand_color = randomcolor.RandomColor()

    self.snake_color = rand_color.generate(hue="red", luminosity="light")[0]
    self.snake_color = ImageColor.getrgb(self.snake_color)
    self.apple_color = None
    self.black_color = (0, 0, 0)

    print self.snake_color

    self.image = None
    self.pix = None

  def clear_screen(self):
    self.image = Image.new("RGB", (self.width, self.height))
    self.pix = self.image.load()

  def reset(self):

    self.clear_screen()
    self.new_apple()

  def new_apple(self):

    rand_color = randomcolor.RandomColor()

    self.apple_color = rand_color.generate(hue="green", luminosity="light")[0]
    self.apple_color = ImageColor.getrgb(self.apple_color)

    while True:
      self.apple[0] = random.randint(0, self.width - 1)
      self.apple[1] = random.randint(0, self.height - 1)

      current_color = self.pix[self.apple[0], self.apple[1]]

      # Make sure we're not drawing over anything
      if current_color == self.black_color:
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

    new_snakehead = copy.copy(self.snakehead)

    if self.direction == "UP":
      new_snakehead[1] -= 1
    elif self.direction == "DOWN":
      new_snakehead[1] += 1
    elif self.direction == "LEFT":
      new_snakehead[0] -= 1
    elif self.direction == "RIGHT":
      new_snakehead[0] += 1

    # Wrap around
    if new_snakehead[0] >= self.width:
      new_snakehead[0] = 0
    elif new_snakehead[0] < 0:
      new_snakehead[0] = self.width - 1

    if new_snakehead[1] >= self.height:
      new_snakehead[1] = 0
    elif new_snakehead[1] < 0:
      new_snakehead[1] = self.height - 1

    color = self.pix[new_snakehead[0], new_snakehead[1]]

    if color == self.snake_color:
      self.die()

    self.segments.appendleft(new_snakehead)

    if new_snakehead == self.apple:
      self.segment_count += 1

      if self.segment_count > self.max_segment_count:
        self.segment_count = self.max_segment_count

      self.new_apple()

    # Trim the end of the snake
    while (len(self.segments) > self.segment_count):
      p = self.segments.pop()

    self.snakehead = new_snakehead

  def die(self):
    time.sleep(1)
    self.setup()

  def setup(self):

    self.reset()

    self.snakehead = [self.width / 2, self.height / 2]
    self.direction = "RIGHT"
    self.is_setup = True
    self.segments = deque()
    self.segment_count = 4

  def draw_frame(self):

    if not self.is_setup:
      self.setup()

    self.update()

    self.clear_screen()

    self.pix[self.apple[0], self.apple[1]] = self.apple_color

    for point in list(self.segments):
      self.pix[point[0], point[1]] = self.snake_color

    return self.image, 100
