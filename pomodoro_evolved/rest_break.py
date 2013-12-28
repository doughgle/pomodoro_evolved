from kitchen_timer import KitchenTimer, AlreadyRunningError, TimeAlreadyUp, NotRunningError
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
        self._canSkip = True
        self._timer = KitchenTimer(whenTimeup, durationInMins)
            
    def skip(self):
        '''
        Skips this break forever.
        '''
        if self._canSkip:
            self._state = self.SKIPPED
        else:
            raise BreakCannotBeSkippedOnceStarted()
    
    def start(self):
        '''
        Starts the break counting down from the given durationInMins.
        '''
        if self.wasSkipped():
            raise BreakAlreadySkipped()
        if self._timer.isStopped():
            raise BreakAlreadyTerminated
        
        try:
            self._timer.start()
        except AlreadyRunningError:
            raise BreakAlreadyStarted()
        except TimeAlreadyUp:
            raise BreakAlreadyTerminated()
        else:
            self._canSkip = False
            
    def stop(self):
        '''
        Stops the break forever. Restarting is forbidden.
        '''
        if self.wasSkipped():
            raise BreakAlreadySkipped()

        try:
            self._timer.stop()
        except NotRunningError:
            raise BreakNotStarted()
            
    def isRunning(self):
        return self._timer.isRunning()
    
    def wasSkipped(self):
        return self._state == self.SKIPPED

    @property
    def timeRemaining(self):
        '''
        Returns the time remaining in seconds.
        '''
        return ceil(self._timer.timeRemaining)
