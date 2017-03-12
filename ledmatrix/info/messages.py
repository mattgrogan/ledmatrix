import time
from canvas import canvas
from drawable import Drawable
from device import Viewport
from PIL import Image

class Messages(Drawable):
    """
    Display messages on the screen
    """

    def __init__(self, device):

        msg = "Hello, world! My name is Matt"
        w, h = self.small_font.getsize(msg)
        w += device.width * 2 # Increase so we scroll on and off the screen

        self.device = Viewport(device, w, h)

        with canvas(self.device) as draw:
            draw.text((device.width,0), msg, font=self.small_font)


    def draw_frame(self):

        scrolled = self.device.move_left()

        if not scrolled:
            self.device.set_position((0,0))

        self.device.display()

        return 100
