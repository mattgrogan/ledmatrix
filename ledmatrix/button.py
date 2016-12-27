from __future__ import print_function

import sys
import time

import RPi.GPIO as gpio


class Button(object):
  """ Represent a physical button """

  def __init__(self, name, gpio_pin, led_pin=None):
    """ Initialize the button with a specific gpio pin """

    self.name = name
    self.gpio_pin = gpio_pin
    self.led_pin = led_pin
    self.is_enabled = False
    self.state = Initial_State()

    # Set up the GPIO pins
    gpio.setmode(gpio.BCM)
    gpio.setup(gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

    if self.led_pin is not None:
      gpio.setup(self.led_pin, gpio.OUT)
      self.led_off()

  @property
  def enabled(self):
    return self.is_enabled

  @enabled.setter
  def enabled(self, value):
    if value:
      self.enable()
    else:
      self.disable()

  @property
  def press_duration_ms(self):
    """ Determine how long the button has been pressed """

    return int((time.time() - self.time_pressed) * 1000.0)

  def led_on(self):
    """ Turn the LED on """

    if self.led_pin is not None:
      gpio.output(self.led_pin, gpio.HIGH)

  def led_off(self):
    """ Turn the LED off """

    if self.led_pin is not None:
      gpio.output(self.led_pin, gpio.LOW)

  def led_toggle(self):
    """ Switch the LED """

    if self.led_pin is not None:
      gpio.output(self.led_pin, not gpio.input(self.led_pin))

  def enable(self, *args, **kwargs):
    """ Begin listening to events """

    if not self.is_enabled:
      self.led_on()
      gpio.add_event_detect(self.gpio_pin, gpio.BOTH, bouncetime=20)
      self.is_enabled = True

  def disable(self, *args, **kwargs):
    """ Stop listening to events """

    if self.is_enabled:
      self.led_off()
      gpio.remove_event_detect(self.gpio_pin)
      self.is_enabled = False

  @property
  def event_detected(self):
    """ Return true if the gpio event was detected """

    event = gpio.event_detected(self.gpio_pin)
    status = gpio.input(self.gpio_pin) == gpio.LOW  # Active low

    retval = self.state.run(event, status)
    self.state = self.state.next_state

    return retval

  def test(self, timeout=10):
    """ Test the button """

    self.enable()
    print("Press %s on pin %i within %i seconds" %
          (self.name, self.gpio_pin, timeout))

    for t in range(timeout):
      if self.event_detected:
        print("Click detected!")
        self.led_off()
        return True
      else:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)

    print("Button %s failed." % self.name)
    self.led_off()
    return False


class Initial_State(object):

  def __init__(self):
    self.next_state = self

  def run(self, event_detected, current_input):
    """ Determine if an event should be fired """

    if event_detected:
      if current_input:
        self.next_state = Down_Press()
        # Here the state should be to down press, but no event
        event = "DOWN"
      else:
        # Raise event for the button up event and stay here
        event = "UP"
    else:
      if current_input:
        # We didn't see a down event, so let's just move anyway
        print("Warning: initial state -> down press without event")
        self.next_state = Down_Press()
        event = "DOWN"
      else:
        # Stay here
        event = None

    return event


class Down_Press(object):

  def __init__(self, timeout_ms=2000):
    self.timeout_ms = timeout_ms
    self._start_time = time.time()
    self.next_state = self

  @property
  def elapsed_ms(self):
    return int((time.time() - self._start_time) * 1000.0)

  def run(self, event_detected, current_input):
    if event_detected:
      if current_input:
        # This doesn't make sense
        return "BAD"
      else:
        self.next_state = Initial_State()
        return "UP"
    else:
      if current_input:
        if self.elapsed_ms >= self.timeout_ms:
          print("INFO: Timeout on button press")
          self.next_state = Down_Press()
          return "TIMEOUT"
      else:
        return "This should not happen, right?"
