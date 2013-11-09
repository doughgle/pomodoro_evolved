
class RulesOfTheTechnique(object):
    '''
    Encapsulates the following rules of the Pomodoro technique:
      Begin with a Pomodoro.
      After a Pomodoro, take a rest break.
      After a rest break, start a new Pomodoro.
      Usually a Pomodoro is followed by a short break, except when the long break interval is reached.
      After a decided number of Pomodoros (default=4) a long break will replace the short break.
    '''
      
    EVERY_FOUR_POMODOROS = 4
    
    def __init__(self, pomodoroCls, shortBreakCls, longBreakCls, longBreakInterval=EVERY_FOUR_POMODOROS):        
        self.Pomodoro = pomodoroCls
        self.ShortBreak = shortBreakCls
        self.LongBreak = longBreakCls
        self._completedPomodoros = 0
        self.longBreakInterval = longBreakInterval

    @property
    def longBreakInterval(self):
        return self._longBreakInterval

    @longBreakInterval.setter
    def longBreakInterval(self, newInterval):
        self._longBreakInterval = newInterval
        
    def isLongBreakTime(self):
        return self._completedPomodoros % self.longBreakInterval == 0
        
    def newTimer(self, prevTimer=None):        
        timer = self.Pomodoro()
        if prevTimer is not None:
            if isinstance(prevTimer, self.Pomodoro):
                self._completedPomodoros += 1
                if self.isLongBreakTime():
                    timer = self.LongBreak()
                else:
                    timer = self.ShortBreak()
        
        return timer
