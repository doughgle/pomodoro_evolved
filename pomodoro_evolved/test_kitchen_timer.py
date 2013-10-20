import unittest
from time import sleep
from kitchen_timer import Timer, NotRunningError, AlreadyRunningError    
    
class TestTimer(unittest.TestCase):

    def waitForTimeup(self):
        while not self.timer.isTimeup():
            pass


    def assertRunning(self):
        return self.assertEqual(Timer.running, self.timer.state)

    def assertStopped(self):
        return self.assertEqual(Timer.stopped, self.timer.state)

    def whenTimeup(self):
        self.timeupCalled = True
        
    def setUp(self):        
        self.timer = Timer()        

    def test_afterInitialisation_TimerIsStopped(self):
        self.assertStopped()
    
    def test_stoppingWhenStopped_isANotRunningError(self):        
        self.assertRaises(NotRunningError, self.timer.stop)
            
    def test_afterStarting_TimerIsRunning(self):
        self.timer.start()
        self.assertRunning()
        
    def test_startingWhileRunning_isAAlreadyRunningError(self):
        self.timer.start(duration=3)
        self.assertRaises(AlreadyRunningError, self.timer.start)
    
    def test_afterStarting_timeupIsFalseWhileRunning(self):
        self.timer.start(duration=3)
        self.assertFalse(self.timer.isTimeup())
        
    def test_afterTimerExpires_TimeUpIsTrue(self):
        self.timer.start(duration=0.05)
        sleep(0.1)
        self.assertTrue(self.timer.isTimeup())        
    
    def test_timerCallsBackWhenTimeExpires(self):
        self.timeupCalled = False
        self.timer.start(duration=0.05, whenTimeup=self.whenTimeup)
        sleep(0.1)
        self.assertTrue(self.timeupCalled)
        
    def test_startingWhenTimeupRestartsTheTimer(self):
        self.timer.start(duration=0.05)
        self.waitForTimeup()
        self.timer.start()
        self.assertRunning()
        
    def test_stoppingWhenTimeup_isNotRunningError(self):
        self.timer.start(duration=0.05)
        self.waitForTimeup()
        self.assertRaises(NotRunningError, self.timer.stop)
        
    def test_startingWhenStoppedRestartsTheTimer(self):
        self.timer.start()
        self.timer.stop()        
        self.timer.start()
        self.assertRunning()
                
    def test_afterStoppingARunningTimer_timerIsStopped(self):
        self.timer.start()
        self.timer.stop()
        self.assertStopped()
        
    def test_timeRemainingWhenTimeupIsZero(self):
        self.timer.start(duration=0.01)
        self.waitForTimeup()
        self.assertEqual(0, self.timer.timeRemaining)
        
    def test_timeRemainingWhenStoppedIsAccurateToOneSecond(self):
        elapsed=1
        for duration in (5, 10, 60):            
            self.timer.start(duration)
            sleep(elapsed)
            self.timer.stop()
            self.assertEqual((duration - elapsed), self.timer.timeRemaining)


if __name__ == "__main__":
    unittest.main()
