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
    
    PRECISION_NUM_DECIMAL_PLACES = 1
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    TIMEUP =  "TIMEUP"
    
    def __init__(self):
        self.__stateLock = Lock()
        self.__timeRemainingLock = Lock()
        self.state = self.STOPPED        
        self.timeRemaining = 0
                    
    def start(self, duration=1, whenTimeup=None):
        if self.isRunning():
            raise AlreadyRunningError    
        else:
            self.state = self.RUNNING            
            self.duration = duration
            self._userWhenTimeup = whenTimeup
            self._startTime = self._now()
            self._timer = TTimer(duration, self._whenTimeup)
            self._timer.start()            
        
    def stop(self):
        if self.isRunning():
            self._timer.cancel()
            self.state = self.STOPPED
            self.timeRemaining = self.duration - self._elapsedTime()
        else:
            raise NotRunningError()

    def isRunning(self):
        return self.state == self.RUNNING
                
    def isTimeup(self):
        return self.state == self.TIMEUP

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
            if self.isRunning():
                self._timeRemaining = self.duration - self._elapsedTime()
            return round(self._timeRemaining, self.PRECISION_NUM_DECIMAL_PLACES)
    
    @timeRemaining.setter
    def timeRemaining(self, timeRemaining):
        with self.__timeRemainingLock:
            self._timeRemaining = timeRemaining
                    
    def _whenTimeup(self):
        self.state = self.TIMEUP
        self.timeRemaining = 0
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()    
        
    def _now(self):
        return time()
    
    def _elapsedTime(self):
        return self._now() - self._startTime
