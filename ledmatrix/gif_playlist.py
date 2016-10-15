import glob
import os
import random

from gif_player import Gif_Player


class Gif_Playlist(object):
  """ Playlist of all Gif Files """

  def __init__(self, folder, matrix, randomize=True):
    """ Create a playlist of all files in the folder """

    self.folder = folder
    self.matrix = matrix

    # Store all the generated items
    self.items = []
    self.current_index = 0

    self.load_items()

    if randomize:
      random.shuffle(self.items)

    self.current_item = self.items[self.current_index]

  def load_items(self):
    """ Load all items from a folder """

    files = [name for name in glob.glob(os.path.join(
        self.folder, '*.gif')) if os.path.isfile(os.path.join(self.folder, name))]

    for filename in files:
      self.items.append(Gif_Player(filename, self.matrix))

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

  def draw_frame(self):
    """ Draw the frame of the current image """

    return self.current_item.draw_frame()
