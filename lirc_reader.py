import time

import lirc

sockid = lirc.init("ledmatrix", "./.lircrc", blocking=False)


while True:
  print "listening..."
  print lirc.nextcode()
  time.sleep(0.50)
