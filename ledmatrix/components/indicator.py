from components import Indicator_Frame, Icon, Text, NoScroll_Text


class Indicator(Indicator_Frame):
  """ Object to hold all indicator data """

  def __init__(self, device, data_mapper):

    super(Indicator, self).__init__(device)

    self.data_mapper = data_mapper

    self.is_playlist = True

    # Location Mapping
    self.icon_pos = (0, 0)
    self.icon_text_pos = (14, 3)
    self.line1_pos = (0, 13)
    self.line2_pos = (0, 24)

    # Construct itself
    self.icon(self.data_mapper)
    self.icon_text(self.data_mapper, "line1")
    self.line1(self.data_mapper, "line2", scroll=False)
    self.line2(self.data_mapper, "line3", scroll=True)

  def icon(self, data):
    """ Set the 12x12 icon option """

    icon = Icon.Icon(data)
    self.add_item(icon, self.icon_pos)

  def icon_text(self, data, field):

    icon_text = NoScroll_Text(data, field)
    self.add_item(icon_text, self.icon_text_pos)

  def line1(self, data, field, scroll=True):

    if scroll:
      line1 = Text(data, field)
    else:
      line1 = NoScroll_Text(data, field)

    self.add_item(line1, self.line1_pos)

  def line2(self, data, field, scroll=True):

    if scroll:
      line2 = Text(data, field)
    else:
      line2 = NoScroll_Text(data, field)

    self.add_item(line2, self.line2_pos)
