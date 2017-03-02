from __future__ import division
import math
from drawable import Drawable
from canvas import canvas


class PVector(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        self.x += v.x
        self.y += v.y

    def sub(self, v):
        self.x -= v.x
        self.y -= v.y

    def mult(self, v):
        self.x *= v.x
        self.y *= v.y

    def div(self, n):
        self.x = self.x / n
        self.y = self.y / n

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self):
        self.div(self.mag)

class Mover(object):

    def __init__(self, size, topspeed = None):
        """ Pass tuples """

        self._location = PVector(0, 0)
        self._velocity = PVector(0, 0)
        self._acceleration = PVector(0, 0)

        # How large is our area?
        self.size = size

        # What is the maximum speed?
        self.topspeed = topspeed

    @property
    def location(self):
        return (self._location.x, self._location.y)

    @location.setter
    def location(self, l):
        x, y = l
        self._location = PVector(x, y)

    @property
    def velocity(self):
        return (self._velocity.x, self._velocity.y)

    @velocity.setter
    def velocity(self, v):
        xspeed, yspeed = v
        self._velocity = PVector(xspeed, yspeed)

    @property
    def acceleration(self):
        return (self._acceleration.x, self._acceleration.y)

    @acceleration.setter
    def acceleration(self, a):
        xaccel, yaccel = a
        self._acceleration = PVector(xaccel, yaccel)

    def update_position(self):
        self._velocity.add(self._acceleration)
        self._location.add(self._velocity)
        self.limit(self.topspeed)

    def limit(self, m):

        if m is not None:

            print self._velocity.mag()

            if self._velocity.mag() > m:
                self._velocity.div(m)
                print "Hit max speed"
                # TODO: This is not correct, must review



    def check_edges(self):
        """ Wrap around """

        w, h = self.size

        if self._location.x >= w:
            self._location.x = 0
        elif self._location.x < 0:
            self._location.x = w - 1

        if self._location.y >= h:
            self._location.y = 0
        elif self._location.y < 0:
            self._location.y = h - 1




class Bouncing_Ball(Drawable):
    """ Draw a bouncing ball on the screen """

    def __init__(self, device):

        self.device = device
        x = int(device.width / 2)
        y = int(device.height / 2)
        xspeed = 1
        yspeed = -1.25

        self.ball = Mover(self.device.size, topspeed=2)
        self.ball.location = (x, y)
        self.ball.acceleration = (-0.001, 0.01)
        #self.ball.velocity = (xspeed, yspeed)

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

        self.ball.update_position()
        self.ball.check_edges()

        with canvas(self.device) as draw:

          draw.point(self.ball.location, "#FFFFFF")

        return 20
