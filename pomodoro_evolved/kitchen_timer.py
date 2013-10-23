from threading import Timer as TTimer
from time import time
from threading import Lock

class NotRunningError(Exception): pass
class AlreadyRunningError(Exception): pass


class KitchenTimer(object):
    '''
    Loosely models a clockwork kitchen timer with the following differences:
        You can start the timer with arbitrary duration (e.g. 1.2 seconds).
        The timer calls back a given function when time's up.
        Querying the time remaining has 0.1 second accuracy.
    '''
    
    running = "running"
    stopped = "stopped"
    timeup =  "timeup"
    
    def __init__(self):
        self.__stateLock = Lock()
        self.state = self.stopped        
        self.__timeRemainingLock = Lock()
        self.timeRemaining = 0
                    
    def start(self, duration=1, whenTimeup=None):
        if self.state == self.running:
            raise AlreadyRunningError    
        else:
            self.state = self.running            
            self.timeRemaining = duration
            self._userWhenTimeup = whenTimeup
            self._startTime = self._now()
            self._timer = TTimer(duration, self._whenTimeup)
            self._timer.start()            
        
    def stop(self):
        if self.state == self.running:
            self._timer.cancel()
            self.state = self.stopped
            self.timeRemaining -= self._elapsedTime()
        else:
            raise NotRunningError()
            
    def isTimeup(self):
        if self.state == self.timeup:
            return True
        else:
            return False

    @property
    def state(self):
        with self.__stateLock:
            return self._state
    
    @state.setter
    def state(self, state):
        with self.__stateLock:
            self._state = state
            
    @property
    def timeRemaining(self):
        with self.__timeRemainingLock:
            if self.state == self.running:
                self._timeRemaining -= self._elapsedTime()
            return round(self._timeRemaining, 1)
    
    @timeRemaining.setter
    def timeRemaining(self, timeRemaining):
        with self.__timeRemainingLock:
            self._timeRemaining = timeRemaining
                    
    def _whenTimeup(self):
        self.state = self.timeup
        self.timeRemaining = 0
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()    
        
    def _now(self):
        return time()
    
    def _elapsedTime(self):
        return self._now() - self._startTime
