#Probable violation of the Liskov Substitution Principle.

class RulesOfTheTechnique(object):
    '''
    Encapsulates the following rules of the Pomodoro technique:
      Begin with a Pomodoro.
      After a Pomodoro, take a rest break.
      After a rest break, start a new Pomodoro.
      Rest breaks are usually a short break. However, periodically after a decided number of Pomodoros, the long break interval,
      take a long break instead.
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
