from components import Indicator_Frame, Icon, Text, NoScroll_Text


class Indicator(Indicator_Frame):
  """ Object to hold all indicator data """

  def __init__(self, device):

    super(Indicator, self).__init__(device)

    # Location Mapping
    self.icon_pos = (0, 0)
    self.icon_text_pos = (14, 3)
    self.line1_pos = (0, 13)
    self.line2_pos = (0, 24)

  def icon(self, name, color):
    """ Set the 12x12 icon option """

    icon = Icon.Icon(name, color)
    self.add_item(icon, self.icon_pos)

  def icon_text(self, callback):

    icon_text = NoScroll_Text(callback)
    self.add_item(icon_text, self.icon_text_pos)

  def line1(self, callback, scroll=True):

    if scroll:
      line1 = Text(callback)
    else:
      line1 = NoScroll_Text(callback)

    self.add_item(line1, self.line1_pos)

  def line2(self, callback, scroll=True):

    if scroll:
      line2 = Text(callback)
    else:
      line2 = NoScroll_Text(callback)

    self.add_item(line2, self.line2_pos)
