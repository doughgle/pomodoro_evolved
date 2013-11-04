
class AlreadySkippedError(Exception): pass
class CannotSkipOnceStarted(Exception): pass

class Break(object):
    
    idle =      "idle"
    running =   "running"
    skipped =   "skipped"
    
    def __init__(self):
        self._state = self.idle
        self._durationInMins = 0
        
    def isRunning(self):
        return self._state == self.running
    
    def wasSkipped(self):
        return self._state == self.skipped
    
    def skip(self):
        if self._state == self.idle:
            self._state = self.skipped
        else:
            raise CannotSkipOnceStarted()
    
    def start(self):
        if self._state == self.skipped:
            raise AlreadySkippedError()
        self._state = self.running
        
    @property
    def timeRemaining(self):
        return 0