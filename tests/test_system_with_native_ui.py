from native_ui import NativeUI

if __name__ == "__main__":
    # configure settings for faster system testing
    app = NativeUI(pomodoroDurationInMins=0.05, shortBreakDurationInMins=0.02, longBreakDurationInMins=0.1)
    app.mainloop()
