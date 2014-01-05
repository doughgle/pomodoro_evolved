from kitchen_timer import KitchenTimer, AlreadyRunningError, TimeAlreadyUp, NotRunningError
from math import ceil

class BreakAlreadySkipped(Exception): pass
class BreakCannotBeSkippedOnceStarted(Exception): pass
class BreakAlreadyStarted(Exception): pass
class BreakNotStarted(Exception): pass
class BreakAlreadyTerminated(Exception): pass

class Break(KitchenTimer):
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
        super(Break, self).__init__(whenTimeup, durationInMins)

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
        if self.isStopped():
            raise BreakAlreadyTerminated()
        
        try:
            super(Break, self).start()
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
            super(Break, self).stop()
        except NotRunningError:
            raise BreakNotStarted()
    
    def wasSkipped(self):
        return self._state == self.SKIPPED

    @property
    def timeRemaining(self):
        '''
        Returns the number of whole seconds remaining.
        '''
        return ceil(super(Break, self).timeRemaining)
