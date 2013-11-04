
class AlreadySkippedError(Exception): pass

class ShortBreak(object):
    
    idle =      "idle"
    running =   "running"
    skipped =   "skipped"
    
    def __init__(self):
        self._state = self.idle
        
    def isRunning(self):
        return self._state == self.running
    
    def wasSkipped(self):
        return self._state == self.skipped
    
    def skip(self):
        self._state = self.skipped
    
    def start(self):
        if self._state == self.skipped:
            raise AlreadySkippedError()
        self._state = self.running