"""
Throttle mixin provides good netizen behavior by limiting remote API calls
"""
import datetime
import logging

log = logging.getLogger("ledmatrix")


class Throttle_Mixin(object):

  def every(self, interval, callback):
    """
    Limit the update to a certain number of seconds.
    """

    self._interval = datetime.timedelta(seconds=interval)
    self._callback = callback

    self._next_run = None

    self.last_success = None
    self.last_attempt = None
    self.retries = 0

  def _schedule_next_run(self):
    """
    Determine when to run next time
    """

    if self.retries == 0:
      # Last result was a success, so we'll schedule the full interval
      interval = self._interval
    else:
      backoff_secs = 2 ** self.retries * 60
      interval = datetime.timedelta(seconds=backoff_secs)
      # The new interval should never be longer than the default.
      interval = min(interval, self._interval)

    self._next_run = self.last_attempt + interval
    log.debug("Next update after %s at %s" % (interval, self._next_run))

  def success(self):
    """ Update success variables """

    self.last_success = datetime.datetime.now()
    self.last_attempt = datetime.datetime.now()
    self.retries = 0
    self._schedule_next_run()

  def failure(self):
    """ Update failure variables """

    self.last_attempt = datetime.datetime.now()
    self.retries += 1
    self._schedule_next_run()

  def run_pending(self):
    """ Run the callback if it's pending """

    if self.should_run:
      log.info("Updating data")
      success = self._callback()

      if success:
        self.success()
      else:
        log.error("Failed to update data")
        self.failure()
    else:
      log.debug("Update not required")
      pass

  @property
  def should_run(self):
    """ Return True if we should run """

    # Is this the first time we've run?
    if self._next_run is None:
      return True

    # Has the time expired
    if datetime.datetime.now() > self._next_run:
      return True

    return False
