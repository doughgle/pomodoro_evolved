'''
Copyright 2013 Douglas Hellinger

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import unittest
from time import sleep
from kitchen_timer import KitchenTimer, NotRunningError, AlreadyRunningError    

DEFAULT_TEST_DURATION = 0.01
ENOUGH_TIME_TO_EXPIRE = DEFAULT_TEST_DURATION * 2

class TestKitchenTimer(unittest.TestCase):
    '''Unit tests for Kitchen Timer class.'''

    def waitForTimeup(self):
        while not self.timer.isTimeup():
            pass

    def assertRunning(self):
        return self.assertEqual(KitchenTimer.running, self.timer.state)

    def assertStopped(self):
        return self.assertEqual(KitchenTimer.stopped, self.timer.state)

    def whenTimeup(self):
        self.timeupCalled = True
        
    def setUp(self):        
        self.timer = KitchenTimer()        

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
        self.timer.start(duration=DEFAULT_TEST_DURATION)
        sleep(ENOUGH_TIME_TO_EXPIRE)
        self.assertTrue(self.timer.isTimeup())        
    
    def test_timerCallsBackWhenTimeExpires(self):
        self.timeupCalled = False
        self.timer.start(duration=DEFAULT_TEST_DURATION, whenTimeup=self.whenTimeup)
        sleep(ENOUGH_TIME_TO_EXPIRE)
        self.assertTrue(self.timeupCalled)
        
    def test_startingWhenTimeupRestartsTheTimer(self):
        self.timer.start(duration=DEFAULT_TEST_DURATION)
        self.waitForTimeup()
        self.timer.start()
        self.assertRunning()
        
    def test_stoppingWhenTimeup_isNotRunningError(self):
        self.timer.start(duration=DEFAULT_TEST_DURATION)
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
        self.timer.start(duration=DEFAULT_TEST_DURATION)
        self.waitForTimeup()
        self.assertEqual(0, self.timer.timeRemaining)
        
    def test_timeRemainingWhenStoppedIsAccurateToOneTenthOfASecond(self):
        elapsed=0.1
        for duration in (1, 10, 60):            
            self.timer.start(duration)
            sleep(elapsed)
            self.timer.stop()
            self.assertEqual((duration - elapsed), self.timer.timeRemaining)


if __name__ == "__main__":
    unittest.main()
