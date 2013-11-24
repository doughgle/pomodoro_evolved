from kitchen_timer import KitchenTimer
from utils import minsToSecs
from math import ceil

class BreakAlreadySkipped(Exception): pass
class BreakCannotBeSkippedOnceStarted(Exception): pass
class BreakAlreadyStarted(Exception): pass
class BreakNotStarted(Exception): pass
class BreakAlreadyTerminated(Exception): pass

class Break(object):
    '''
    Models a timed rest break with a default duration of 5 minutes.
    Allows the break to be skipped before starting.
    Does not allow the break to be restarted after time's up or it's stopped.
    '''
    
    IDLE =      "IDLE"
    RUNNING =   "RUNNING"
    SKIPPED =   "SKIPPED"
    STOPPED =   "STOPPED"
    TIMEUP =    "TIMEUP"
    
    def __init__(self, whenTimeup, durationInMins=5):
        self._state = self.IDLE
        self._userWhenTimeup = whenTimeup
        self._durationInMins = durationInMins
        self._timer = KitchenTimer(self._whenTimeup, durationInMins)
            
    def skip(self):
        '''
        Skips this break forever.
        '''
        if self._state == self.IDLE:
            self._state = self.SKIPPED
        else:
            raise BreakCannotBeSkippedOnceStarted()
    
    def start(self):
        '''
        Starts the break counting down from the given durationInMins.
        '''
        if self._state == self.IDLE:
            self._timer.start()
            self._state = self.RUNNING
        elif self.wasSkipped():
            raise BreakAlreadySkipped()
        elif self.isRunning():
            raise BreakAlreadyStarted()
        else:
            raise BreakAlreadyTerminated()
            
    def stop(self):
        '''
        Stops the break forever. Restarting is forbidden.
        '''
        if self.wasSkipped():
            raise BreakAlreadySkipped()
        elif not self.isRunning():
            raise BreakNotStarted()
        else:
            self._timer.stop()
            self._state = self.STOPPED
            
    def isRunning(self):
        return self._state == self.RUNNING
    
    def wasSkipped(self):
        return self._state == self.SKIPPED

    @property
    def timeRemaining(self):
        '''
        Returns the time remaining in seconds.
        '''
        if self._state == self.IDLE:
            return ceil(minsToSecs(self._durationInMins))
        else:
            return ceil(self._timer.timeRemaining)
    
    def _whenTimeup(self):
        self._state = self.TIMEUP
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()
