import Tkinter as tk
from pomodoro import Pomodoro
from datetime import timedelta

class NativeUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)
        self.label.pack()
        self.pomodoro = Pomodoro(self.whenTimeup, durationInMins=0.1)
        self.pomodoro.start()
        self.update_display(self.pomodoro.timeRemaining)

    def whenTimeup(self):
        print "time's up!"
        
    def update_display(self, remaining=None):
        self.label.configure(text=str(timedelta(seconds=self.pomodoro.timeRemaining)))
        self.after(1000, self.update_display)

if __name__ == "__main__":
    app = NativeUI()
    app.mainloop()
