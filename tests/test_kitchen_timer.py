import unittest
from time import sleep
from kitchen_timer import KitchenTimer
from kitchen_timer import NotRunningError, AlreadyRunningError, TimeAlreadyUp
from kitchen_timer import NotStartedError
from utils import minsToSecs

DEFAULT_TEST_DURATION_MINS = 0.0005 #about 30ms yaybo
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


class KitchenTimerConcurrencyTests(unittest.TestCase):
    '''Concurrency Tests for Kitchen Timer class.'''
    
    def setUp(self):
        self.timer = KitchenTimer(whenTimeup=self.timeupCallback, durationInMins=DEFAULT_TEST_DURATION_MINS)

    def timeupCallback(self):
        self.timeupCalled = True
            
    def test_whatIfStopIsCalledByAnotherThreadJustAsTimesUp(self):
        self.timeupCalled = False
        self.timer = MockKitchenTimer(whenTimeup=self.timeupCallback, durationInMins=DEFAULT_TEST_DURATION_MINS)
        # The timer thread will block when the timer expires, but before the callback
        # is invoked.
#        thread_1 = threading.Thread(target=self.timer.start)
#        thread_1.start()
        self.timer.start()
        self.assertTrue(self.timer.isRunning())
        sleep(0.05)
        
        # The timer is now blocked at _whenTimeup. In the parent thread, we stop it.
        self.timer.stop()
        self.assertTrue(self.timer.isStopped())
        
        # Now allow the callback thread to resume.
        self.timer.resume()
        sleep(0.1)
        self.assertFalse(self.timeupCalled, "timeup callback shouldn't have been called after stopping.")
        self.assertTrue(self.timer.isStopped())
        self.assertFalse(self.timer.isRunning())
        self.assertFalse(self.timer.isTimeup())
        
    def test_whatIfIsRunningIsQueriedByAnotherThreadImmediatelyAfterStarting(self):
        # TODO: needs to guarantee the race condition.
        self.timeupCalled = False
        self.timer = MockKitchenTimer(whenTimeup=self.timeupCallback, durationInMins=DEFAULT_TEST_DURATION_MINS)        
        thread_1 = threading.Thread(target=self.timer.start)
        thread_1.start()
        self.assertTrue(self.timer.isRunning())
        
    def test_stateIsUpdateAtomically_soIdleRunningStoppedTimeup_areMutuallyExclusive(self):
        pass

        
from time import time

class TestTimeStampingBehaviour(unittest.TestCase):
    '''Tests the time stamping of various timer state transitions.'''
    
    def test_queryingStartTimeWhenNotYetStarted_isANotStartedError(self):
        timer = KitchenTimer()
        self.assertRaises(NotStartedError, getattr, timer, 'startedAt')
        
    def test_afterStarting_timeAndDateShouldBeLogged(self):
        timer = KitchenTimer()
        timeBeforeStarting = time()
        timer.start()
        self.assertEqual(timeBeforeStarting, timer.startedAt)

import threading

class MockKitchenTimer(KitchenTimer):

    _runningLock = threading.Condition()

    def __init__(self, whenTimeup=None, durationInMins=1):
        super(MockKitchenTimer, self).__init__(whenTimeup, durationInMins)
    
    def _whenTimeup(self):
        '''
        Note that a call to wait releases the lock.
        '''
        with self._runningLock:
            self._runningLock.wait()
        KitchenTimer._whenTimeup(self)

    def resume(self):
        with self._runningLock:
            self._runningLock.notify()





if __name__ == "__main__":
    unittest.main()
