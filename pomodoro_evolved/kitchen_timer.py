from threading import Timer as TTimer


class NotRunningError(Exception): pass
class AlreadyRunningError(Exception): pass


class Timer(object):
    
    running = "running"
    stopped = "stopped"
    timeup = "timeup"
    
    def __init__(self):
        self.state = self.stopped        
            
    def start(self, duration=1, whenTimeup=None):
        if self.state == self.running:
            raise AlreadyRunningError    
        else:
            self._timer = TTimer(duration, self._whenTimeup)
            self._timer.start()            
            self.state = self.running            
            self._userWhenTimeup = whenTimeup
        
    def stop(self):
        if self.state == self.running:
            self.state = self.stopped
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
        