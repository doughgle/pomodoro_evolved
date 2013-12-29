from threading import Timer, Lock
from time import time
from utils import minsToSecs
from datetime import datetime

class NotStartedError(Exception): pass
class NotRunningError(Exception): pass
class NotEndedError(Exception): pass
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
            self._userWhenTimeup = whenTimeup
            self._durationInSecs = minsToSecs(durationInMins)
            self._timeRemaining = 0
                    
    def start(self):
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
                self._startedAt = time()
                self._timer = Timer(self._durationInSecs, self._whenTimeup)
                self._timer.start()
        
    def stop(self):
        '''
        Stops the timer, preventing whenTimeup callback.
        '''
        with self._stateLock:
            if self.isRunning():
                self._timer.cancel()
                self._state = self.STOPPED
                self._timeRemaining = self._durationInSecs - self._elapsedTime()
            else:
                raise NotRunningError()

    def isRunning(self):
        return self._state == self.RUNNING
                
    def isStopped(self):
        return self._state == self.STOPPED
    
    def isTimeup(self):
        return self._state == self.TIMEUP
            
    def addToLog(self, timerLog):
        '''Adds itself to the given timerLog.'''
        timerLog.add(name=self.__class__.__name__, startedAt=self.startedAt, endedAt=self.endedAt)
        print self.__class__.__name__,
        print "started: ", datetime.fromtimestamp(self.startedAt).strftime('%a %x %H:%M:%S'),
        print "ended: ", datetime.fromtimestamp(self.endedAt).strftime('%H:%M:%S')

    @property
    def timeRemaining(self):
        '''
        Returns the time remaining in seconds. Gives fractions of a second if the system clock allows.
        '''
        if self._state == self.IDLE:
            return self._durationInSecs
        if self.isRunning():
            self._timeRemaining = self._durationInSecs - self._elapsedTime()
        return self._timeRemaining
    
    @property
    def startedAt(self):
        '''
        Returns the time this timer was started in Unix timestamp format.
        '''
        try:
            return self._startedAt
        except AttributeError:
            raise NotStartedError()
        
    @property
    def endedAt(self):
        '''
        Returns the time this timer ended (stopped or timeup) in Unix timestamp format.
        '''
        try:
            return self._endedAt
        except AttributeError:
            raise NotEndedError()
                    
    def _whenTimeup(self):
        with self._stateLock:
            if self.isRunning():
                self._state = self.TIMEUP
                self._endedAt = time()
                self._timeRemaining = 0
                if callable(self._userWhenTimeup):
                    self._userWhenTimeup()
            
    def _elapsedTime(self):
        return time() - self._startedAt
