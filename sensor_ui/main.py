# This code handles the user interface for the sensor box
from __future__ import division

import time
from Adafruit_LED_Backpack import AlphaNum4
import influxdb
import iso8601      # for date string -> date object
from datetime import datetime


INFLUX_HOST = "ledmatrix"
INFLUX_DB = "home"

class Sensor_UI(object):

    def __init__(self):

        self.dbclient = influxdb.InfluxDBClient(INFLUX_HOST, 8086, database=INFLUX_DB)

        self.displays = []
        start_addr = 0x70

        for i in range(4):
            addr = start_addr + i
            disp = AlphaNum4.AlphaNum4(address=addr)
            disp.begin()
            disp.set_brightness(5)
            disp.clear()
            self.displays.append(disp)

    def identify(self):
        """ Identify the displays """

        for i, disp in enumerate(self.displays):
            disp.print_str(str(i))
            disp.write_display()

    def show_temp(self):

        # Write out temp and humidity
        # ---------------------------

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
            last_update_str = "NOW"
        else:
            last_update_str = "%im" % (last_update_secs / 60)

        temp_f = round(d["temp_f"])
        humidity = round(d["humidity"])

        self.displays[0].print_str("TEMP")
        self.displays[2].print_str("%i f" % temp_f)

        self.displays[1].print_str(last_update_str)
        self.displays[3].print_str("%irh" % humidity)

        for disp in self.displays:
            disp.write_display()

if __name__ == "__main__":

    ui = Sensor_UI()
    ui.identify()
    time.sleep(0.25)
    ui.show_temp()
