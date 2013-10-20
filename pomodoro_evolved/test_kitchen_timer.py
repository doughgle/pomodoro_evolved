import unittest
from time import sleep
from threading import Timer as TTimer

idle = "idle"
running = "running"
stopped = "stopped"
timeup = "timeup"

class NotRunningError(Exception): pass
class AlreadyRunningError(Exception): pass
    
class Timer(object):
    
    def __init__(self):
        self.state = idle        
            
    def start(self, duration=1, whenTimeup=None):
        if self.state == idle or self.state == timeup or self.state == stopped:
            self._timer = TTimer(duration, self._whenTimeup)
            self._timer.start()            
            self.state = running            
            self._userWhenTimeup = whenTimeup
        elif self.state == running:
            raise AlreadyRunningError    
    
    def _whenTimeup(self):
        self.state = timeup
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()    
    
    def stop(self):
        if self.state == running:
            self.state = stopped
        else:
            raise NotRunningError()
            
    def isTimeup(self):
        if self.state == timeup:
            return True
        else:
            return False 
            
    def reset(self):
        pass
    
    
class TestTimer(unittest.TestCase):

    def assertRunning(self):
        return self.assertEqual(running, self.timer.state)


    def assertIdle(self):
        return self.assertEqual(idle, self.timer.state)

    def assertStopped(self):
        return self.assertEqual(stopped, self.timer.state)

    def whenTimeup(self):
        self.timeupCalled = True
        
    def setUp(self):        
        self.timer = Timer()        

    def test_afterInitialisation_TimerIsIdle(self):
        self.assertIdle()
    
    def test_stoppingWhenIdle_isANotRunningError(self):        
        self.assertRaises(NotRunningError, self.timer.stop)
            
    def test_afterStartingFromIdle_TimerIsRunning(self):
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
        while not self.timer.isTimeup():
            pass
        self.timer.start()
        self.assertRunning()
        
    def test_stoppingWhenTimeup_isNotRunningError(self):
        self.timer.start(duration=0.05)
        while not self.timer.isTimeup():
            pass
        self.assertRaises(NotRunningError, self.timer.stop)
        
    def test_startingWhenStoppedRestartsTheTimer(self):
        self.timer.start()
        self.timer.stop()        
        self.timer.start()
        self.assertRunning()
        
    def test_resettingFromIdle_DoesNothing(self):
        self.timer.reset()
        self.assertIdle()
                
    def test_afterStoppingARunningTimer_timerIsStopped(self):
        self.timer.start()
        self.timer.stop()
        self.assertStopped()


if __name__ == "__main__":
    unittest.main()
