import unittest
from short_break import ShortBreak, AlreadySkippedError

class TestShortBreak(unittest.TestCase):

    def assertRunning(self):
        return self.assertTrue(self.shortBreak.isRunning())


    def setUp(self):
        self.shortBreak = ShortBreak()        
    
    def test_afterCreationShortBreakIsNotRunning(self):
        self.assertFalse(self.shortBreak.isRunning())
        
    def test_afterCreationShortBreakIsNotSkipped(self):
        self.assertFalse(self.shortBreak.wasSkipped())        
        
    def test_afterSkipping_wasSkippedReturnsTrue(self):
        self.shortBreak.skip()
        self.assertTrue(self.shortBreak.wasSkipped())
        
    def test_afterSkipping_startingAShortBreakIsAAlreadySkippedError(self):
        self.shortBreak.skip()
        self.assertRaises(AlreadySkippedError, self.shortBreak.start)
    
    def test_afterStarting_isRunningReturnsTrue(self):
        self.shortBreak.start()
        self.assertRunning()
        


if __name__ == "__main__":
    unittest.main()