import influxdb

import logging
import logging.handlers


from utils.throttle_mixin import Throttle_Mixin

log = logging.getLogger("ledmatrix")
logging.basicConfig()
log.setLevel(logging.DEBUG)


class InfluxDB(Throttle_Mixin):
  """
  Retrieve data from InfluxDB
  """

  def __init__(self, query, host, db, port=8086, timeout=0.5):

    self.query = query

    self.dbclient = influxdb.InfluxDBClient(
        host, port, database=db, timeout=timeout)

    self._results = {}

    self.every(60 * 5, self.update)

  def __getitem__(self, key):

    # Call mixin
    self.run_pending()

    if key in self._results.keys():
      val = self._results[key]
    else:
      val = ""

    return val

  def update(self):

    try:
      rs = self.dbclient.query(self.query)
    except:
      log.exception("Exception")
      return False

    data = list(rs.get_points())
    self._results = data[0]

    return True


if __name__ == "__main__":

  query = """ SELECT
                      "temp_f" AS "temp_f",
                      "humidity" as "humidity"
                  FROM "home"."autogen"."SI7201 Temp+Humidity"
                  ORDER BY DESC
                  LIMIT 1
      """

  db = InfluxDB(query, "ledmatrix", "home")
  print db["temp_f"]
