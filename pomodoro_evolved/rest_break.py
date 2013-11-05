from kitchen_timer import KitchenTimer
from pomodoro import minsToSecs

class BreakAlreadySkipped(Exception): pass
class CannotSkipOnceStarted(Exception): pass
class BreakAlreadyStarted(Exception): pass
class BreakNotStarted(Exception): pass

class Break(object):
    
    idle =      "idle"
    running =   "running"
    skipped =   "skipped"
    stopped =   "stopped"
    
    def __init__(self, whenTimeup, durationInMins=5):
        self._state = self.idle
        self._durationInMins = durationInMins
        self._whenTimeup = whenTimeup
        self._timer = KitchenTimer()
            
    def skip(self):
        if self._state == self.idle:
            self._state = self.skipped
        else:
            raise CannotSkipOnceStarted()
    
    def start(self):
        if self._state == self.skipped:
            raise BreakAlreadySkipped()
        elif self._state == self.running:
            raise BreakAlreadyStarted()
        else:
            self._timer.start(minsToSecs(self._durationInMins), self._whenTimeup)
            self._state = self.running
            
    def stop(self):
        if self._state == self.skipped:
            raise BreakAlreadySkipped()
        elif self._state != self.running:
            raise BreakNotStarted()
        else:
            self._timer.stop()
            self._state = self.stopped
            
    def isRunning(self):
        return self._state == self.running
    
    def wasSkipped(self):
        return self._state == self.skipped

    @property
    def timeRemaining(self):
        return minsToSecs(self._durationInMins)
