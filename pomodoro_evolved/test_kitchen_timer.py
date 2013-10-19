import unittest

idle = "idle"
running = "running"
stopped = "stopped"

class Timer(object):
    
    def __init__(self):
        self.state = idle
        
    def start(self):
        if self.state == idle:
            self.state = running
    
    def stop(self):
        if self.state == running:
            self.state = stopped
            
    def reset(self):
        pass
    
    

class TestTimer(unittest.TestCase):

    def assertIdle(self):
        return self.assertEqual(idle, self.timer.state)

    def assertStopped(self):
        return self.assertEqual(stopped, self.timer.state)

    def setUp(self):
        self.timer = Timer()        


    def test_afterInitialisation_TimerIsIdle(self):
        self.assertEqual(idle, self.timer.state)
        
    def test_stoppingFromIdle_DoesNothing(self):
        self.timer.stop()
        self.assertEqual(idle, self.timer.state)
        
    def test_resettingFromIdle_DoesNothing(self):
        self.timer.reset()
        self.assertIdle()
        
    def test_afterStartingFromIdle_TimerIsRunning(self):
        self.timer.start()
        self.assertEqual(running, self.timer.state)
        
    def test_afterStoppingARunningTimer_timerIsStopped(self):
        self.timer.start()
        self.timer.stop()
        self.assertStopped()
        
    def test_startingFromStopped_DoesNothing(self):
        self.timer.start()
        self.timer.stop()
        self.timer.start()
        self.assertStopped()
        
        
        


if __name__ == "__main__":
    unittest.main()