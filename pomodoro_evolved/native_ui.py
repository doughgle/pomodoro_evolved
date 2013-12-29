import Tkinter as tk
import tkFont
import tkMessageBox
from pomodoro import Pomodoro
from datetime import timedelta, datetime
from Queue import Queue, Empty
from rest_break import Break as ShortBreak
from rest_break import Break as LongBreak
from test_time_logger import MockTimerLog as TimerLog

class NativeUI(tk.Tk):
    
    def __init__(self, pomodoroDurationInMins=25, shortBreakDurationInMins=5, longBreakDurationInMins=15):
        tk.Tk.__init__(self)
        self.clockFont = tkFont.Font(family="Helvetica", size=18)
        self.clock = tk.Label(self, width=15, font=self.clockFont)
        self.startStopButton = tk.Button(self)
        self.clock.pack()
        self.startStopButton.pack()
        self.uiQueue = Queue()
        self._handleUiRequest()
        self._completedPomodoros = 0
        self._pomodoroDurationInMins = pomodoroDurationInMins
        self._shortBreakDurationInMins = shortBreakDurationInMins
        self._longBreakDurationInMins = longBreakDurationInMins
        self._timerLog = TimerLog()
        self.newTimer()
    
    def isLongBreakTime(self):
        return self._completedPomodoros % 4 == 0
    
    def newTimer(self, prevTimer=None):
        '''
        Set's up the next timer, whether it's a Pomodoro or a Break
        '''
        self.timer = Pomodoro(self.whenTimeup, durationInMins=self._pomodoroDurationInMins)
        self.timerName = "Pomodoro"
        if prevTimer is not None:
            # addToLog status of prevTimer before creating a new one.
            prevTimer.addToLog(self._timerLog)            
            
            if isinstance(prevTimer, Pomodoro):
                self._completedPomodoros += 1
                if self.isLongBreakTime():
                    self.timer = LongBreak(self.whenTimeup, durationInMins=self._longBreakDurationInMins)
                    self.timerName = "Long Break"
                else:
                    self.timer = ShortBreak(self.whenTimeup, durationInMins=self._shortBreakDurationInMins)
                    self.timerName = "Short Break"
        
        self.title(self.timerName)
        self.clock.configure(text=str(timedelta(seconds=self.timer.timeRemaining)))
        self.startStopButton.configure(text="Start", command=self.onStart)
        
    def onStart(self):
        self.timer.start()
        self.drawClock()
        self.startStopButton.configure(text="Stop", command=self.onStop)
        print "started %s!" % self.timerName
        
    def onStop(self):
        if tkMessageBox.askyesno("", "Void this %s?" % self.timerName):
            if self.timer.isRunning():
                self.timer.stop()
                print "stopped!"
                self.newTimer(self.timer)

    def whenTimeup(self):
        '''
        Called by the timer in a separate thread when time's up.
        '''
        print "timeup!"
        uiFunction = (tkMessageBox.showinfo, ("time's up", "%s Complete!" % self.timerName), {})
        self.uiQueue.put(uiFunction)
        self.newTimer(self.timer)
                
    def drawClock(self):
        if self.timer.isRunning():
            self.clock.configure(text=str(timedelta(seconds=self.timer.timeRemaining)))
            self.after(1000, self.drawClock)
            
    def _handleUiRequest(self):
        '''
        Services the UI queue to handles UI requests in the main thread.
        '''
        try:
            while True:
                f, a, k = self.uiQueue.get_nowait()
                f(*a, **k)
        except Empty:
            pass
        
        self.after(200, self._handleUiRequest)

if __name__ == "__main__":
    app = NativeUI()
    app.mainloop()
