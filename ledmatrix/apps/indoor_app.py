from datetime import datetime
import iso8601  # for date string -> date object

import influxdb

from components import Indicator_App, Icon, Text, NoScroll_Text, Indicator_Frame


class Indoor_App(Indicator_App):
  """
  Show indoor conditions from sensor database
  """

  def __init__(self, device, dbclient):

    super(Indoor_App, self).__init__(device)

    self.device = device
    self.dbclient = dbclient

    self.timeout = 1 * 60  # Pickup every minute
    self._last_attempt = None

    # Build frame
    icon = Icon.Icon("lightning")
    text1 = NoScroll_Text(self.temp, font="MEDIUM", color="#88fc95")
    text2 = NoScroll_Text(self.rh, font="MEDIUM", color="#88fc95")
    text3 = NoScroll_Text(self.last_update, font="MEDIUM", color="#444444")

    # Frame
    f = Indicator_Frame(device)
    f.add_item(icon, (1, 1))
    f.add_item(text1, (icon.size[0] + 2, 4))
    f.add_item(text2, (0, icon.size[1] + 1))
    f.add_item(text3, (0, icon.size[1] + 2 + text1.size[1]))

    self.add_frame(f)
    self.add_frame(Indicator_Frame(device))

  def _timeout_expired(self):
    """
    Determines if the timeout since last attempt has expired.
    """

    # This is the first attempt
    if self._last_attempt is None:
      return True

    # How many seconds since the last attempt?
    delta = (datetime.now() - self._last_attempt).total_seconds()

    return delta > self.timeout

  def update_data(self):
    """
    Grab new data from influx
    """

    self._last_attempt = datetime.now()

    query = """ SELECT
                        "temp_f" AS "temp_f",
                        "humidity" as "humidity"
                    FROM "home"."autogen"."SI7201 Temp+Humidity"
                    ORDER BY DESC
                    LIMIT 1
        """
    rs = self.dbclient.query(query)
    data = list(rs.get_points())
    d = data[0]

    time_string = d["time"]
    now = datetime.utcnow()
    then = iso8601.parse_date(time_string, default_timezone=None)

    then = then.replace(tzinfo=None)

    self.last_update_secs = (now - then).total_seconds()

    self.temp_f = round(d["temp_f"])
    self.humidity = round(d["humidity"])

  def temp(self):

    if self._timeout_expired():
      self.update_data()

    # Drop the decimal point
    temp = "%iF" % self.temp_f

    return temp

  def rh(self):

    if self._timeout_expired():
      self.update_data()

    # Drop the decimal point
    rh = "%i%% RH" % self.humidity

    return rh

  def last_update(self):

    if self.last_update_secs < 120:
      last_update_str = "NOW"
    else:
      last_update_str = "%iM AGO" % (last_update_secs / 60)

    return last_update_str
