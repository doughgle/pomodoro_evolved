from threading import Timer, Lock
from time import time
from utils import minsToSecs

class NotRunningError(Exception): pass
class AlreadyRunningError(Exception): pass
class TimeAlreadyUp(Exception): pass


class KitchenTimer(object):
    '''
    Loosely models a clockwork kitchen timer with the following differences:
        You can start the timer with arbitrary duration (e.g. 1.25 seconds).
        The timer calls back a given function when time's up.
        Querying the time remaining returns fractions of a second if the system clock allows.
    '''

    IDLE =    "IDLE"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    TIMEUP  = "TIMEUP"
    
    def __init__(self, whenTimeup=None, durationInMins=1):
        self._stateLock = Lock()
        with self._stateLock:
            self._state = self.IDLE
            self._durationInMins = durationInMins
            self._timeRemaining = 0
                    
    def start(self, duration=1, whenTimeup=None):
        '''
        Starts the timer to count down from the given duration and call whenTimeup when time's up.
        '''
        with self._stateLock:
            if self.isRunning():
                raise AlreadyRunningError
            elif self.isTimeup():
                raise TimeAlreadyUp()
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
                self._timeRemaining = self.duration - self._elapsedTime()
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
        '''
        Returns the time remaining in seconds.
        '''
        if self._state == self.IDLE:
            return minsToSecs(self._durationInMins)
        if self.isRunning():
            self._timeRemaining = self.duration - self._elapsedTime()
        return self._timeRemaining
                    
    def _whenTimeup(self):
        with self._stateLock:
            self._state = self.TIMEUP
            self._timeRemaining = 0
            if callable(self._userWhenTimeup):
                self._userWhenTimeup()
        
    def _elapsedTime(self):
        return time() - self._startTime
