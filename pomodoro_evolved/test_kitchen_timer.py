import unittest

class KitchenTimer(object):
    
    def __init__(self):
        self.state = "Stopped"
        
    def stop(self):
        pass
    

class TestTimer(unittest.TestCase):

    def setUp(self):
        self.timer = KitchenTimer()        

    def test_afterInitialisationTimerIsStopped(self):
        self.assertEqual("Stopped", self.timer.state)
        
    def test_stoppingAStoppedTimerDoesNothingToItsState(self):
        self.timer.stop()
        self.assertEqual("Stopped", self.timer.state)


if __name__ == "__main__":
    unittest.main()