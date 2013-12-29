from native_ui import NativeUI

if __name__ == "__main__":
    # configure settings for faster system testing
    app = NativeUI(pomodoroDurationInMins=0.01, shortBreakDurationInMins=0.01, longBreakDurationInMins=0.01)
    app.mainloop()
