import unittest
from pomodoro import Pomodoro, PomodoroNotRunning, PomodoroAlreadyStarted

class TestPomodoro(unittest.TestCase):

    def whenTimeup(self):
        self.timeUp = True
        
    def setUp(self):
        self.pomodoro = Pomodoro(self.whenTimeup)

    def test_afterCreation_pomodoroIsNotRunning(self):
        self.assertFalse(self.pomodoro.isRunning())
        
    def test_afterCreation_pomodoroIsNotInterrupted(self):
        self.assertFalse(self.pomodoro.wasInterrupted())
        
    def test_interruptingAPomodoroThatIsNotRunningIsANotRunningException(self):
        self.assertRaises(PomodoroNotRunning, self.pomodoro.interrupt)
        
    def test_startingAPomodoroThatIsAlreadyStartedIsAnAlreadyStartedException(self):
        self.pomodoro.start()
        self.assertRaises(PomodoroAlreadyStarted, self.pomodoro.start)

    def test_afterStarting_PomodoroCallsBackWhenTimesUp(self):
        self.timeUp = False
        self.pomodoro.start()
        self.assertTrue(self.timeUp)
        

if __name__ == "__main__":
    unittest.main()