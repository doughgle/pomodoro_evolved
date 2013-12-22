from kitchen_timer import KitchenTimer
from kitchen_timer import NotRunningError, AlreadyRunningError
from math import ceil

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
        self._timer = KitchenTimer(whenTimeup, durationInMins)
            
    def start(self):
        try:
            self._timer.start()
        except AlreadyRunningError:
            raise PomodoroAlreadyStarted()
                                
    def stop(self):
        try:
            self._timer.stop()
        except NotRunningError:
            raise PomodoroNotRunning()

    def isRunning(self):
        return self._timer.isRunning()
        
    def wasInterrupted(self):
        return self._timer.isStopped()

    @property
    def timeRemaining(self):
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
