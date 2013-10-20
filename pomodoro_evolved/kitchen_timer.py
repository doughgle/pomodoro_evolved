from threading import Timer as TTimer
from time import time

class NotRunningError(Exception): pass
class AlreadyRunningError(Exception): pass


class Timer(object):
    
    running = "running"
    stopped = "stopped"
    timeup =  "timeup"
    
    def __init__(self):
        self.state = self.stopped        
        self.timeRemaining = 0
            
    def start(self, duration=1, whenTimeup=None):
        if self.state == self.running:
            raise AlreadyRunningError    
        else:
            self.timeRemaining = round(duration, 1)
            self._startTime = self._now()
            self._timer = TTimer(duration, self._whenTimeup)
            self._timer.start()            
            self.state = self.running            
            self._userWhenTimeup = whenTimeup
        
    def stop(self):
        if self.state == self.running:
            self.state = self.stopped
            self.timeRemaining -= round(self._elapsedTime(), 1)
        else:
            raise NotRunningError()
            
    def isTimeup(self):
        if self.state == self.timeup:
            return True
        else:
            return False
        
    def _whenTimeup(self):
        self.state = self.timeup
        self.timeRemaining = 0
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()    
        
    def _now(self):
        return time()
    
    def _elapsedTime(self):
        return self._now() - self._startTime

