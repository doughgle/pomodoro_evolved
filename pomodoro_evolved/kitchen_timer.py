from threading import Timer, Lock
from time import time

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
    TIMEUP  = "TIMEUP"
    
    def __init__(self):
        self._stateLock = Lock()
        with self._stateLock:
            self._state = self.STOPPED
            self.timeRemaining = 0
                    
    def start(self, duration=1, whenTimeup=None):
        '''
        Starts the timer to count down from the given duration and call whenTimeup when time's up.
        '''
        with self._stateLock:
            if self.isRunning():
                raise AlreadyRunningError
            else:
                self._state = self.RUNNING
                self.duration = duration
                self._userWhenTimeup = whenTimeup
                self._startTime = time()
                self._timer = Timer(duration, self._whenTimeup)
                self._timer.start()
        
    def stop(self):
        '''
        Stops the timer, preventing whenTimeup callback.
        '''
        with self._stateLock:
            if self.isRunning():
                self._timer.cancel()
                self._state = self.STOPPED
                self.timeRemaining = self.duration - self._elapsedTime()
            else:
                raise NotRunningError()

    def isRunning(self):
        return self._state == self.RUNNING
                
    def isStopped(self):
        return self._state == self.STOPPED
    
    def isTimeup(self):
        return self._state == self.TIMEUP
            
    @property
    def timeRemaining(self):
        if self.isRunning():
            self._timeRemaining = self.duration - self._elapsedTime()
        return round(self._timeRemaining, self.PRECISION_NUM_DECIMAL_PLACES)
    
    @timeRemaining.setter
    def timeRemaining(self, timeRemaining):
        self._timeRemaining = timeRemaining
                    
    def _whenTimeup(self):
        with self._stateLock:
            self._state = self.TIMEUP
            self.timeRemaining = 0
            if callable(self._userWhenTimeup):
                self._userWhenTimeup()
        
    def _elapsedTime(self):
        return time() - self._startTime
