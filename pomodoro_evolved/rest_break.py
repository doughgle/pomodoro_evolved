from kitchen_timer import KitchenTimer
from pomodoro import minsToSecs
from math import ceil

class BreakAlreadySkipped(Exception): pass
class CannotSkipOnceStarted(Exception): pass
class BreakAlreadyStarted(Exception): pass
class BreakNotStarted(Exception): pass
class BreakAlreadyTerminated(Exception): pass

class Break(object):
    
    IDLE =      "IDLE"
    RUNNING =   "RUNNING"
    SKIPPED =   "SKIPPED"
    STOPPED =   "STOPPED"
    TIMEUP =    "TIMEUP"
    
    def __init__(self, whenTimeup, durationInMins=5):
        self._state = self.IDLE
        self._durationInMins = durationInMins
        self._userWhenTimeup = whenTimeup
        self._timer = KitchenTimer()
            
    def skip(self):
        if self._state == self.IDLE:
            self._state = self.SKIPPED
        else:
            raise CannotSkipOnceStarted()
    
    def start(self):
        if self._state == self.IDLE:
            self._timer.start(minsToSecs(self._durationInMins), self._whenTimeup)
            self._state = self.RUNNING
        elif self._state == self.SKIPPED:
            raise BreakAlreadySkipped()
        elif self._state == self.RUNNING:
            raise BreakAlreadyStarted()
        else:
            raise BreakAlreadyTerminated()
            
    def stop(self):
        if self._state == self.SKIPPED:
            raise BreakAlreadySkipped()
        elif self._state != self.RUNNING:
            raise BreakNotStarted()
        else:
            self._timer.stop()
            self._state = self.STOPPED
            
    def isRunning(self):
        return self._state == self.RUNNING
    
    def wasSkipped(self):
        return self._state == self.SKIPPED

    @property
    def timeRemaining(self):
        if self._state == self.IDLE:
            return minsToSecs(self._durationInMins)
        else:
            return ceil(self._timer.timeRemaining)
    
    def _whenTimeup(self):
        self._state = self.TIMEUP
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()
