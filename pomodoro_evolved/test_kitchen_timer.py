import unittest
from time import sleep
from threading import Timer as TTimer

idle = "idle"
running = "running"
stopped = "stopped"
timeup = "timeup"

class Timer(object):
    
    def __init__(self):
        self.state = idle        
            
    def start(self, duration=1, whenTimeup=None):
        if self.state == idle:
            self._timer = TTimer(duration, self._whenTimeup)
            self._timer.start()            
            self.state = running            
            self._userWhenTimeup = whenTimeup
    
    def _whenTimeup(self):
        self.state = timeup
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()    
    
    def stop(self):
        if self.state == running:
            self.state = stopped
            
    def isTimeup(self):
        if self.state == timeup:
            return True
        else:
            return False 
            
    def reset(self):
        pass
    
    
class TestTimer(unittest.TestCase):

    def assertIdle(self):
        return self.assertEqual(idle, self.timer.state)

    def assertStopped(self):
        return self.assertEqual(stopped, self.timer.state)

    def whenTimeup(self):
        self.timeupCalled = True
        
    def setUp(self):        
        self.timer = Timer()        

    def test_afterInitialisation_TimerIsIdle(self):
        self.assertEqual(idle, self.timer.state)
        
    def test_afterStartingFromIdle_TimerIsRunning(self):
        self.timer.start()
        self.assertEqual(running, self.timer.state)

    def test_afterTimerExpires_StateIsTimeUp(self):
        self.timer.start(duration=0.1)
        sleep(0.2)
        self.assertTrue(self.timer.isTimeup())
    
    def test_afterStarting_timeupIsFalseUntilTimeup(self):
        self.timer.start(duration=3)
        self.assertFalse(self.timer.isTimeup())
    
    def test_timerCallsBackWhenTimeExpires(self):
        self.timeupCalled = False
        self.timer.start(duration=0.1, whenTimeup=self.whenTimeup)
        sleep(0.2)
        self.assertTrue(self.timeupCalled)
    
    def test_stoppingFromIdle_DoesNothing(self):
        self.timer.stop()
        self.assertEqual(idle, self.timer.state)
        
    def test_resettingFromIdle_DoesNothing(self):
        self.timer.reset()
        self.assertIdle()
        
        
    def test_afterStoppingARunningTimer_timerIsStopped(self):
        self.timer.start()
        self.timer.stop()
        self.assertStopped()
        
        
        


if __name__ == "__main__":
    unittest.main()
