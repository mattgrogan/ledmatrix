import time


class Rpi_UI(object):

  def __init__(self, controller):

    self.controller = controller

    from matrix_adapter import Adafruit_Matrix_Adapter
    self.controller.matrix = Adafruit_Matrix_Adapter()

    from remote_control import Remote_Control

    self.rc = Remote_Control()
    self.rc.register(u"KEY_STOP", controller, controller.handle_stop)
    self.rc.register(u"KEY_UP", controller, controller.handle_up)
    self.rc.register(u"KEY_DOWN", controller, controller.handle_down)
    self.rc.register(u"KEY_LEFT", controller, controller.handle_left)
    self.rc.register(u"KEY_RIGHT", controller, controller.handle_right)

  def mainloop(self):

    while True:
      delay = self.controller.run(self.rc)
      time.sleep(delay)
