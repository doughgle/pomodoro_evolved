import Tkinter as tk
import tkFont
from pomodoro import Pomodoro
from datetime import timedelta

class NativeUI(tk.Tk):
    def __init__(self):
        self.pomodoro = Pomodoro(self.whenTimeup, durationInMins=0.1)
        tk.Tk.__init__(self)
        self.clockFont = tkFont.Font(family="Helvetica", size=18)
        self.label = tk.Label(self, text=str(timedelta(seconds=self.pomodoro.timeRemaining)), width=10, font=self.clockFont)
        self.label.pack()
        self.startButton = tk.Button(self, text ="Start", command=self.onStart)
        self.startButton.pack()

    def whenTimeup(self):
        print "time's up!"
        
    def onStart(self):
        self.pomodoro.start()
        self.update_display(self.pomodoro.timeRemaining)
        print "started!"
        
    def update_display(self, remaining=None):
        self.label.configure(text=str(timedelta(seconds=self.pomodoro.timeRemaining)))
        self.after(1000, self.update_display)

if __name__ == "__main__":
    app = NativeUI()
    app.mainloop()
