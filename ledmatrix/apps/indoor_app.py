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
    text = Text(self.text)

    # Frame
    f = Indicator_Frame(device)
    f.add_item(icon, (1, 1))
    f.add_item(text, (0, icon.size[1] + 1))

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

    print "Time string: %s" % d["time"]
    print "Now: %s" % now
    print "Then: %s" % then

    last_update_secs = (now - then).total_seconds()

    if last_update_secs < 120:
      self.last_update_str = "NOW"
    else:
      self.last_update_str = "%im" % (last_update_secs / 60)

    self.temp_f = round(d["temp_f"])
    self.humidity = round(d["humidity"])

  def text(self):
    if self._timeout_expired():
      self.update_data()

    text = "Indoor temp: "
    text += str(self.temp_f)
    text += "  RH: "
    text += str(self.humidity)
    text += "%  "
    text += self.last_update_str

    return text
