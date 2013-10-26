from kitchen_timer import KitchenTimer

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
    
    def __init__(self, whenTimeup, durationInMins=25):        
        self._isRunning = False
        self._wasInterrupted = False
        self._whenTimeup = whenTimeup
        self._durationInMins = durationInMins
        self._timer = KitchenTimer()
        
    def isRunning(self):
        return self._isRunning
        
    def wasInterrupted(self):
        return self._wasInterrupted
    
    def start(self):
        if self.isRunning():
            raise PomodoroAlreadyStarted()
        else:
            self._isRunning = True
            self._timer.start(whenTimeup=self._whenTimeup, duration=minsToSecs(self._durationInMins))
                
    def interrupt(self):
        if not self.isRunning():
            raise PomodoroNotRunning()
        else:
            self._timer.stop()
            self._isRunning = False
            self._wasInterrupted = True

    @property
    def timeRemaining(self):
        return self._timer.timeRemaining
        
if __name__ == '__main__':
    def whenTimeup():
        print "timeup!"
        
    pp = Pomodoro(whenTimeup, durationInMins=0.1)
    print pp.timeRemaining
    pp.start()    
    print pp.timeRemaining
    