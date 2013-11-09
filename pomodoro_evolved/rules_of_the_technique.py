
class RulesOfTheTechnique(object):
    
    def __init__(self, pomodoro, shortBreak, longBreak):
        self._completedPomodoros = 0
        self.Pomodoro = pomodoro
        self.ShortBreak = shortBreak
        self.LongBreak = longBreak

    def isLongBreakTime(self):
        return self._completedPomodoros % 4 == 0
        
    def newTimer(self, prevTimer=None):        
        timer = self.Pomodoro()
        if prevTimer is not None:
            if prevTimer.type == "Pomodoro":
                self._completedPomodoros += 1
                if self.isLongBreakTime():
                    timer = self.LongBreak()
                else:
                    timer = self.ShortBreak()
        
        return timer
