
class PomodoroNotRunning(Exception): pass
class PomodoroAlreadyStarted(Exception): pass

class Pomodoro(object):
    '''
    A Pomodoro is the indivisable unit of time used to work on a task.
    After starting, the Pomodoro is running until:
      a) You complete it.
      b) You interrupt it.
    '''
    
    def __init__(self, whenTimeup):
        self.__isRunning = False
        self._whenTimeup = whenTimeup
        
    def isRunning(self):
        return self.__isRunning
        
    def wasInterrupted(self):
        return False
    
    def start(self):
        if self.isRunning():
            raise PomodoroAlreadyStarted()
        else:
            self.__isRunning = True
            if callable(self._whenTimeup):
                self._whenTimeup()
                
    def interrupt(self):
        raise PomodoroNotRunning()