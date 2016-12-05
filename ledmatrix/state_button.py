import time

import RPi.GPIO as gpio


class State_Button(object):

  def __init__(self, name, gpio_pin):

    self.name = name
    self.gpio_pin = gpio_pin
    self.state = Button_Idle()

    # Set up the GPIO pins
    gpio.setmode(gpio.BCM)
    gpio.setup(gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(self.gpio_pin, gpio.FALLING)  # , bouncetime=5)

  @property
  def event_detected(self):

    event_detected = gpio.event_detected(self.gpio_pin)
    button_level = gpio.input(self.gpio_pin) == gpio.LOW  # Active LOW

    if event_detected:
      button_state = "RELEASE"
    else:
      if button_level:
        button_state = "HOLD"
      else:
        button_state = "OPEN"

    event = self.state.check_state(button_state)
    self.state = self.state.next_state

    return event


class Button_Idle(object):

  def __init__(self):
    self._start_time = time.time
    self.next_state = self

  def check_state(self, button_event):

    if button_event == "RELEASE":
      # Button was pressed and released
      self.next_state = Button_Up_1()
    if button_event == "HOLD":
      # Button is pressed currently
      self.next_state = Button_Down_1()

    return None  # No event to return


class Button_Down_1(object):
  """ Button is down for the first time """

  def __init__(self, timeout_ms=100):

    self._timeout_ms = timeout_ms
    self._start_time = time.time()
    self.next_state = self

  @property
  def _timeout(self):
    return int((time.time() - self._start_time) * 1000.0) > self._timeout_ms

  def check_state(self, button_event):

    event = None

    if button_event in ["RELEASE", "OPEN"]:
      self.next_state = Button_Up_1()

    if button_event == "HOLD":
      if self._timeout:
        event = "BUTTON_PRESS"
        self.next_state = Button_Holding()

    return event


class Button_Up_1(object):
  """ Listening for a double click """

  def __init__(self, timeout_ms=100):

    self._timeout_ms = timeout_ms
    self._start_time = time.time()
    self.next_state = self

  @property
  def _timeout(self):
    return int((time.time() - self._start_time) * 1000.0) > self._timeout_ms

  def check_state(self, button_event):

    event = None

    if button_event == "RELEASE":
      event = "BUTTON_DOUBLE_CLICK"
      self.next_state = Button_Idle()
    elif button_event == "HOLD":
      self.next_state = Button_Down_1()
    elif self._timeout:
      event = "BUTTON_CLICK"
      self.next_state = Button_Idle()

    return event


class Button_Down_2(object):
  """ Listening for a double click """

  def __init__(self):

    self._timeout_ms = timeout_ms
    self._start_time = time.time()
    self.next_state = self

  def check_state(self, button_event):

    event = None

    if button_event == "RELEASE":
      event = "BUTTON_DOUBLE_CLICK"
      self.next_state = Button_Idle()

    return event


class Button_Holding(object):

  def __init__(self, timeout_ms=10000):

    self._timeout_ms = timeout_ms
    self._timeout_fired = False
    self._start_time = time.time()
    self.next_state = self

  @property
  def _timeout(self):
    return int((time.time() - self._start_time) * 1000.0) > self._timeout_ms

  def check_state(self, button_event):

    event = None

    if button_event == "HOLD":
      if self._timeout and not self._timeout_fired:
        event = "BUTTON_TIMEOUT"
        self._timeout_fired = True
    else:
      event = "BUTTON_RELEASE"
      self.next_state = Button_Idle()

    return event
