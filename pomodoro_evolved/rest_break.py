from kitchen_timer import KitchenTimer
from pomodoro import minsToSecs

class AlreadySkippedError(Exception): pass
class CannotSkipOnceStarted(Exception): pass
class BreakAlreadyStarted(Exception): pass

class Break(object):
    
    idle =      "idle"
    running =   "running"
    skipped =   "skipped"
    
    def __init__(self, whenTimeup, durationInMins=5):
        self._state = self.idle
        self._durationInMins = 0
        self._whenTimeup = whenTimeup
        self._timer = KitchenTimer()
            
    def skip(self):
        if self._state == self.idle:
            self._state = self.skipped
        else:
            raise CannotSkipOnceStarted()
    
    def start(self):
        if self._state == self.skipped:
            raise AlreadySkippedError()
        elif self._state == self.running:
            raise BreakAlreadyStarted()
        else:
            self._timer.start(minsToSecs(self._durationInMins), self._whenTimeup)
            self._state = self.running            
        
    def isRunning(self):
        return self._state == self.running
    
    def wasSkipped(self):
        return self._state == self.skipped

    @property
    def timeRemaining(self):
        return 0