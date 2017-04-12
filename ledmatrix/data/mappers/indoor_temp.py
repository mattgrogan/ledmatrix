import time
from data.utils.indicator_mapper import Indicator_Data_Map
from data.influx import InfluxDB

INFLUX_HOST = "ledmatrix"
INFLUX_DB = "home"


class Indoor_Mapper(Indicator_Data_Map):
  """ Mapper for inside conditions """

  def __init__(self):

    query = """ SELECT
                        "temp_f" AS "temp_f",
                        "humidity" as "humidity"
                    FROM "home"."autogen"."SI7201 Temp+Humidity"
                    ORDER BY DESC
                    LIMIT 1
        """

    self._data = InfluxDB(query, INFLUX_HOST, INFLUX_DB)

    self.init()

    text = lambda: "%iF %i%% RH" % (
        self._data["temp_f"],
        self._data["humidity"]
    )

    self["icon_name"] = "house"
    self["icon_color"] = "#85144B"
    self["line1"] = ""
    self["line2"] = lambda: time.strftime(
        "%I:%M", time.localtime()).lstrip("0")
    self["line3"] = text
