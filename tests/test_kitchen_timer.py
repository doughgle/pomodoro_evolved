import unittest
from time import sleep
from kitchen_timer import KitchenTimer
from kitchen_timer import NotRunningError, AlreadyRunningError, TimeAlreadyUp
from utils import minsToSecs

DEFAULT_TEST_DURATION_MINS = 0.0005
ENOUGH_TIME_TO_EXPIRE = DEFAULT_TEST_DURATION_MINS * 60 * 2

class TestKitchenTimer(unittest.TestCase):
    '''Unit tests for Kitchen Timer class.'''

    def setUp(self):
        self.timer = KitchenTimer(self.whenTimeup, durationInMins=DEFAULT_TEST_DURATION_MINS)
        
    def waitForTimeup(self):
        while not self.timer.isTimeup():
            pass

    def assertRunning(self):
        self.assertTrue(self.timer.isRunning())
        self.assertFalse(self.timer.isStopped())
        self.assertFalse(self.timer.isTimeup())

    def assertStopped(self):
        self.assertTrue(self.timer.isStopped())
        self.assertFalse(self.timer.isRunning())
        self.assertFalse(self.timer.isTimeup())

    def assertTimeup(self):
        self.assertTrue(self.timer.isTimeup())
        self.assertFalse(self.timer.isRunning())
        self.assertFalse(self.timer.isStopped())
    
    def whenTimeup(self):
        self.timeupCalled = True

    def test_afterInitialisation_TimerIsNotRunning(self):
        self.assertFalse(self.timer.isRunning())
        
    def test_afterInitialisation_TimerIsNotStopped(self):
        self.assertFalse(self.timer.isStopped())
    
    def test_afterInitialisation_TimerIsNotTimeup(self):
        self.assertFalse(self.timer.isTimeup())
                        
    def test_afterInitialisation_timeRemainingInSecondsIsEquivalentToDurationInMins(self):
        self.assertEqual(self.timer._durationInSecs, self.timer.timeRemaining)

    def test_afterStarting_TimerIsRunning(self):
        self.timer.start()
        self.assertRunning()

    def test_startingWhileRunning_isAAlreadyRunningError(self):
        self.timer.start()
        self.assertRaises(AlreadyRunningError, self.timer.start)

    def test_afterStarting_timeupIsFalseWhileRunning(self):
        self.timer.start()
        self.assertFalse(self.timer.isTimeup())

    def test_afterTimerExpires_TimeUpIsTrue(self):
        self.timer.start()
        sleep(ENOUGH_TIME_TO_EXPIRE)
        self.assertTimeup()

    def test_timerCallsBackWhenTimeExpires(self):
        self.timeupCalled = False
        self.timer.start()
        sleep(ENOUGH_TIME_TO_EXPIRE)
        self.assertTrue(self.timeupCalled)
        
    def test_startingAfterTimeup_isATimerAlreadyFinishedException(self):
        self.timer.start()
        self.waitForTimeup()
        self.assertRaises(TimeAlreadyUp, self.timer.start)
        
    def test_stoppingWhenTimeup_isNotRunningError(self):
        self.timer.start()
        self.waitForTimeup()
        self.assertRaises(NotRunningError, self.timer.stop)
        
    def test_stoppingWhenStopped_isANotRunningError(self):
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
        
    def test_afterStopping_timerDoesNotCallback(self):
        self.timeupCalled = False
        self.timer.start()
        self.timer.stop()
        sleep(ENOUGH_TIME_TO_EXPIRE)
        self.assertFalse(self.timeupCalled, "whenTimeup should not have been called")
                
    def test_afterStarting_timerShouldNotCallBackBeforeTimesup(self):
        self.timeupCalled = False
        self.timer.start()
        sleep(0.01)
        self.assertFalse(self.timeupCalled)
                        
    def test_afterTimeup_timeRemainingIsZero(self):
        self.timer.start()
        self.waitForTimeup()
        self.assertEqual(0, self.timer.timeRemaining)
        
    def test_canQueryTimeRemainingWhenStopped(self):
        elapsed = 0.1
        for duration in (1, 10, 60):
            self.timer = KitchenTimer(durationInMins=duration)
            self.timer.start()
            sleep(elapsed)
            self.timer.stop()
            self.assertEqual((minsToSecs(duration) - elapsed), round(self.timer.timeRemaining, 1))
            
    def test_canQueryTimeRemainingWhileTimerIsRunning(self):
        elapsed = 0.05
        duration = 3
        self.timer = KitchenTimer(durationInMins=duration)
        self.timer.start()
        for i in range(1, 4):
            sleep(elapsed)
            self.assertEqual((minsToSecs(duration) - (elapsed * i)), round(self.timer.timeRemaining, 2))
            
    def test_whatHappensWhenTheDurationIsVeryFast(self):
        self.skipTest("unable to reproduce race condition")
        self.timer.start(0.001)
        sleep(0.0005)
        self.timer.stop()
        self.assertEqual(0, self.timer.timeRemaining)
        self.assertTimeup()


class KitchenTimerConcurrencyTests(unittest.TestCase):
    '''Concurrency Tests for Kitchen Timer class.'''
    
    def setUp(self):
        self.timer = KitchenTimer()
        
    def test_ifStoppedBeforeTimeup_isStoppedShouldAlwaysBeTrue(self):
        self.skipTest("unable to reliably reproduce race condition")
        for duration in (DEFAULT_TEST_DURATION_MINS,
                         DEFAULT_TEST_DURATION_MINS / 10,
                         DEFAULT_TEST_DURATION_MINS / 100,
                         DEFAULT_TEST_DURATION_MINS / 1000,
                         DEFAULT_TEST_DURATION_MINS / 10000):
            self.timer.start(duration)
            self.timer.stop()
            self.assertTrue(self.timer.isStopped())
            self.assertFalse(self.timer.isRunning())
            self.assertFalse(self.timer.isTimeup())

if __name__ == "__main__":
    unittest.main()
