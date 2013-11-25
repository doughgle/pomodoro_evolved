from kitchen_timer import KitchenTimer
from math import ceil
from utils import minsToSecs

class PomodoroNotRunning(Exception): pass
class PomodoroAlreadyStarted(Exception): pass


class Pomodoro(object):
    '''
    A Pomodoro is the indivisable unit of time used to work on a task.
    After starting, the Pomodoro is running until:
      a) You complete it.
      b) You stop it.
    '''
    
    IDLE =          "IDLE"
    RUNNING =       "RUNNING"
    INTERRUPTED =   "INTERRUPTED"
    COMPLETED =     "COMPLETED"
    
    def __init__(self, whenTimeup, durationInMins=25):
        self._state = self.IDLE
        self._userWhenTimeup = whenTimeup
        self._durationInMins = durationInMins
        self._timer = KitchenTimer(self._whenTimeup, durationInMins)
            
    def start(self):
        if self.isRunning():
            raise PomodoroAlreadyStarted()
        else:
            self._state = self.RUNNING
            self._timer.start()
                    
    def stop(self):
        if not self.isRunning():
            raise PomodoroNotRunning()
        else:
            self._timer.stop()
            self._state = self.INTERRUPTED

    def isRunning(self):
        return self._state == self.RUNNING
        
    def wasInterrupted(self):
        return self._state == self.INTERRUPTED

    @property
    def timeRemaining(self):
        if self._state == self.IDLE:
            return ceil(minsToSecs(self._durationInMins))
        else:
            return ceil(self._timer.timeRemaining)
        
    def _whenTimeup(self):
        self._state = self.COMPLETED
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()
        
if __name__ == '__main__':
    '''
    This example starts a 1 minute Pomodoro and prints "timeup!" when it completes.
    '''
    from time import sleep, strftime, gmtime
    import sys
    
    def whenTimeup():
        print "timeup!"
        
    pp = Pomodoro(whenTimeup, durationInMins=1)
    pp.start()
    print "running Pomodoro..."
    while pp.isRunning():
        sys.stdout.write(strftime('%M:%S', gmtime(pp.timeRemaining)) + '\r')
        sys.stdout.flush()
        sleep(1)
