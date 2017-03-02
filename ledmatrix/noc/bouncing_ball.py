from drawable import Drawable
from canvas import canvas


class pvector(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        self.x += v.x
        self.y += v.y


class Bouncing_Ball(Drawable):
    """ Draw a bouncing ball on the screen """

    def __init__(self, device):

        self.device = device
        self.location = pvector(int(device.width / 2), int(device.height / 2))
        self.velocity = pvector(1, -1.25)

    def update_position(self):

        self.location.add(self.velocity)

        if self.location.x <= 0:
            self.location.x = 0
            self.velocity.x *= -1

        if self.location.x >= self.device.width - 1:
            self.location.x = self.device.width - 1
            self.velocity.x *= -1

        if self.location.y <= 0:
            self.location.y = 0
            self.velocity.y *= -1

        if self.location.y >= self.device.height - 1:
            self.location.y = self.device.height - 1
            self.velocity.y *= -1

    def draw_frame(self):

        self.update_position()

        with canvas(self.device) as draw:

          draw.point((self.location.x, self.location.y), "#FFFFFF")

        return 200
