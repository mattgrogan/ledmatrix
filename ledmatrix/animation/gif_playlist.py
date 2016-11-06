import glob
import os
import random

from gif_player import Gif_Player

TIMEOUT_MS = 1000


class Gif_Playlist(object):
  """ Playlist of all Gif Files """

  def __init__(self, folder, playmode="RANDOM", timeout_ms=TIMEOUT_MS):
    """ Create a playlist of all files in the folder """

    self.folder = folder
    self.playmode = playmode  # "RANDOM" "NORMAL"
    self.timeout_ms = timeout_ms

    # Store all the generated items
    self.items = []
    self.current_index = 0

    self.load_items()

    self.current_item = self.items[self.current_index]

  @property
  def is_finished(self):
    """ Is the current item finished playing? """

    return self.current_item.is_finished

  def load_items(self):
    """ Load all items from a folder """

    files = [name for name in glob.glob(os.path.join(
        self.folder, '*.gif')) if os.path.isfile(os.path.join(self.folder, name))]

    for filename in files:
      self.items.append(Gif_Player(filename))

    if len(self.items) == 0:
      raise ValueError("No GIF images found in %s" % self.folder)

  def move(self, step=1):
    """ Move to next image """

    self.current_index += step

    if self.current_index >= len(self.items):
      self.current_index = 0
    elif self.current_index < 0:
      self.current_index = len(self.items) - 1

    self.current_item = self.items[self.current_index]
    self.current_item.start(timeout_ms=self.timeout_ms)

  def move_random(self):
    """ Find a random gif image """

    self.current_index = random.randint(0, len(self.items))
    self.current_item = self.items[self.current_index]
    self.current_item.start(timeout_ms=self.timeout_ms)

  def draw_frame(self):
    """ Draw the frame of the current image """

    if self.playmode == "RANDOM" and self.current_item.is_finished:
      self.move_random()

    return self.current_item.draw_frame()
