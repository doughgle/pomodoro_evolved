
class RulesOfTheTechnique(object):
    
    EVERY_FOUR_POMODOROS = 4
    
    def __init__(self, pomodoro, shortBreak, longBreak, longBreakInterval=EVERY_FOUR_POMODOROS):
        self.Pomodoro = pomodoro
        self.ShortBreak = shortBreak
        self.LongBreak = longBreak
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
