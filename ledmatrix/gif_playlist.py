import glob
import os

from gif_player import Gif_Player


class Gif_Playlist(object):
  """ Playlist of all Gif Files """

  def __init__(self, folder, matrix):
    """ Create a playlist of all files in the folder """

    self.images = []

    self.folder = folder

    self.files = [name for name in glob.glob(os.path.join(
        self.folder, '*.gif')) if os.path.isfile(os.path.join(self.folder, name))]

    for filename in self.files:
      self.images.append(Gif_Player(filename, matrix))

    self.current_index = 0
    # TODO: Ensure that there's an image for this index

  def move_next(self):
    """ Move to next image """

    self.current_index += 1

    if self.current_index >= len(self.images):
      self.current_index = 0

  def draw_frame(self):
    """ Draw the frame of the current image """

    return self.images[self.current_index].draw_frame()
