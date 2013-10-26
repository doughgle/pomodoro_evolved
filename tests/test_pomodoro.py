import unittest
from pomodoro import Pomodoro, PomodoroNotRunning, PomodoroAlreadyStarted
from time import sleep

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
        self.pomodoro = Pomodoro(self.whenTimeup, 0.001)
        self.pomodoro.start()
        sleep(0.1)
        self.assertTrue(self.timeUp)
        
    def test_afterStarting_isRunningReturnsTrue(self):
        self.pomodoro.start()
        self.assertTrue(self.pomodoro.isRunning())
    
    def test_afterInterrupting_wasInterruptedReturnsTrue(self):
        self.pomodoro.start()
        self.pomodoro.interrupt()
        self.assertTrue(self.pomodoro.wasInterrupted())
                
    def test_afterPomodoroIsInterrupted_itWillNoLongerCallBack(self):
        self.timeUp = False
        self.pomodoro = Pomodoro(self.whenTimeup, 0.001)
        self.pomodoro.start()
        self.pomodoro.interrupt()
        sleep(0.1)
        self.assertFalse(self.timeUp, "whenTimeup should not have been called")
    
    def test_afterInterrupting_isRunningReturnsFalse(self):
        self.pomodoro.start()
        self.pomodoro.interrupt()
        self.assertFalse(self.pomodoro.isRunning())
        
    def test_canQueryTimeRemainingAtSecondIntervals(self):
        self.assertEqual(0, self.pomodoro.timeRemaining)
        self.pomodoro.start()        
        self.assertEqual(1500, self.pomodoro.timeRemaining)

if __name__ == "__main__":
    unittest.main()
