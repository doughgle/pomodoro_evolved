from kitchen_timer import KitchenTimer
from math import ceil

class PomodoroNotRunning(Exception): pass
class PomodoroAlreadyStarted(Exception): pass

def minsToSecs(mins):
    return mins * 60

class Pomodoro(object):
    '''
    A Pomodoro is the indivisable unit of time used to work on a task.
    After starting, the Pomodoro is running until:
      a) You complete it.
      b) You interrupt it.
    '''
    
    IDLE =          "idle"
    RUNNING =       "running"
    INTERRUPTED =   "interrupted"
    COMPLETED =     "completed"
    
    def __init__(self, whenTimeup, durationInMins=25):
        self._state = self.IDLE
        self._userWhenTimeup = whenTimeup
        self._durationInMins = durationInMins
        self._timer = KitchenTimer()
        
    def isRunning(self):
        return self._state == self.RUNNING
        
    def wasInterrupted(self):
        return self._state == self.INTERRUPTED
    
    def start(self):
        if self.isRunning():
            raise PomodoroAlreadyStarted()
        else:
            self._state = self.RUNNING
            self._timer.start(whenTimeup=self._whenTimeup, duration=minsToSecs(self._durationInMins))
                
    def _whenTimeup(self):
        self._state = self.COMPLETED
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()
    
    def interrupt(self):
        if not self.isRunning():
            raise PomodoroNotRunning()
        else:
            self._timer.stop()
            self._state = self.INTERRUPTED

    @property
    def timeRemaining(self):
        if self._state == self.IDLE:
            return minsToSecs(self._durationInMins)
        else:
            return ceil(self._timer.timeRemaining)
        
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
