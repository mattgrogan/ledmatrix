import glob
import os
import random
import logging


from gif_player import Gif_Player
from menu import Menu

TIMEOUT_MS = 1000

log = logging.getLogger("ledmatrix")


class Gif_Playlist(object):
  """ Playlist of all Gif Files """

  def __init__(self, device, folder, timeout_ms=TIMEOUT_MS):
    """ Create a playlist of all files in the folder """

    self.device = device

    self.folder = folder
    self.timeout_ms = timeout_ms
    self.items = Menu()

    self.load_items()

    self.is_playlist = True

  @property
  def is_finished(self):
    """ Is the current item finished playing? """

    return self.items.current_item.is_finished

  def load_items(self):
    """ Load all items from a folder """

    files = [name for name in glob.glob(os.path.join(
        self.folder, '*.gif')) if os.path.isfile(os.path.join(self.folder, name))]

    random.shuffle(files)

    for filename in files:
      self.items.append(filename, Gif_Player(filename))

    if len(self.items) == 0:
      raise ValueError("No GIF images found in %s" % self.folder)

  def handle_input(self, command):

    if command == "LEFT":
      self.items.next()
      self.items.current_item.start(self.timeout_ms)
    elif command == "RIGHT":
      self.items.prev()
      self.items.current_item.start(self.timeout_ms)

  def draw_frame(self):
    """ Draw the frame of the current image """

    if self.items.current_item.is_finished:
      self.items.next()
      log.info("Starting: %s", self.items.current_item_name)
      self.items.current_item.start(self.timeout_ms)

    im, dur = self.items.current_item.draw_frame()

    self.device.image = im
    self.device.display()

    return dur
