import Tkinter as tk
import tkFont
import tkMessageBox
from pomodoro import Pomodoro
from datetime import timedelta

class NativeUI(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.clockFont = tkFont.Font(family="Helvetica", size=18)
        self.label = tk.Label(self, width=10, font=self.clockFont)
        self.startStopButton = tk.Button(self)
        self.label.pack()
        self.startStopButton.pack()
        self.newPomodoro()

    def newPomodoro(self):
        self.pomodoro = Pomodoro(self.whenTimeup, durationInMins=0.05)
        self.label.configure(text=str(timedelta(seconds=self.pomodoro.timeRemaining)))
        self.startStopButton.configure(text="Start", command=self.onStart)
    
    def whenTimeup(self):
        print "timeup!"
        tkMessageBox.showinfo(message="Pomodoro Complete!")
        self.newPomodoro()
        
    def onStart(self):
        self.pomodoro.start()
        self.update_display(self.pomodoro.timeRemaining)
        self.startStopButton.configure(text="Stop", command=self.onStop)
        print "started!"
        
    def onStop(self):        
        if tkMessageBox.askyesno("", "Void this Pomodoro?"):
            self.pomodoro.interrupt()
            print "stopped!"
            self.newPomodoro()
        
    def update_display(self, remaining=None):
        if self.pomodoro.isRunning():
            self.label.configure(text=str(timedelta(seconds=self.pomodoro.timeRemaining)))
            self.after(1000, self.update_display)

if __name__ == "__main__":
    app = NativeUI()
    app.mainloop()
