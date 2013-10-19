import unittest

class KitchenTimer(object):
    
    def __init__(self):
        self.state = "Stopped"

class Test(unittest.TestCase):


    def test_afterInitialisationTimerIsStopped(self):
        timer = KitchenTimer()
        self.assertEqual("Stopped", timer.state)


if __name__ == "__main__":
    unittest.main()