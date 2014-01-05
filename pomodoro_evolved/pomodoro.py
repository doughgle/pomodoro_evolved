from kitchen_timer import KitchenTimer
from kitchen_timer import NotRunningError, AlreadyRunningError
from math import ceil

class PomodoroNotRunning(Exception): pass
class PomodoroAlreadyStarted(Exception): pass


class Pomodoro(KitchenTimer):
    '''
    A Pomodoro is the indivisable unit of time used to work on a task.
    After starting, the Pomodoro is running until:
      a) You complete it.
      b) You stop it.
    '''    
    
    def __init__(self, whenTimeup, durationInMins=25, name='Pomodoro'):
        super(Pomodoro, self).__init__(whenTimeup, durationInMins, name)
            
    def start(self):
        try:
            super(Pomodoro, self).start()
        except AlreadyRunningError:
            raise PomodoroAlreadyStarted()
                                
    def stop(self):
        try:
            super(Pomodoro, self).stop()
        except NotRunningError:
            raise PomodoroNotRunning()
       
    def wasInterrupted(self):
        return super(Pomodoro, self).isStopped()

    @property
    def timeRemaining(self):
        '''Returns the number of whole seconds remaining.'''
        return ceil(super(Pomodoro, self).timeRemaining)

        
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
