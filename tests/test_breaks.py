import unittest
from rest_break import Break
from rest_break import AlreadySkippedError, CannotSkipOnceStarted, BreakAlreadyStarted

class TestShortBreak(unittest.TestCase):

    def assertRunning(self):
        return self.assertTrue(self.shortBreak.isRunning())

    def assertPostCondition_onceSkippedCanNeverBeRunning(self):
        return self.assertNotEqual(self.shortBreak.isRunning(), self.shortBreak.wasSkipped())
    
    def setUp(self):
        self.shortBreak = Break()        
    
    def test_afterCreationShortBreakIsNotRunning(self):
        self.assertFalse(self.shortBreak.isRunning())
        
    def test_afterCreationShortBreakIsNotSkipped(self):
        self.assertFalse(self.shortBreak.wasSkipped())        
    
    def test_afterCreation_timeRemainingInSecondsIsEquivalentToDurationInMinutes(self):
        self.assertEqual((self.shortBreak._durationInMins * 60), self.shortBreak.timeRemaining)
            
    def test_afterSkipping_wasSkippedReturnsTrue(self):
        self.shortBreak.skip()
        self.assertTrue(self.shortBreak.wasSkipped())
        self.assertPostCondition_onceSkippedCanNeverBeRunning()
        
    def test_afterSkipping_startingAShortBreakIsAnAlreadySkippedError(self):
        self.shortBreak.skip()
        self.assertRaises(AlreadySkippedError, self.shortBreak.start)
        self.assertPostCondition_onceSkippedCanNeverBeRunning()
    
    def test_afterStarting_isRunningReturnsTrue(self):
        self.shortBreak.start()
        self.assertRunning()
        self.assertFalse(self.shortBreak.wasSkipped())
        
    def test_afterStarting_skippingABreakIsACannotSkipBreakOnceStarted(self):
        self.shortBreak.start()
        self.assertRaises(CannotSkipOnceStarted, self.shortBreak.skip)
        
    def test_startingABreakThatIsAlreadyStartedIsAnAlreadyStartedException(self):
        self.shortBreak.start()
        self.assertRaises(BreakAlreadyStarted, self.shortBreak.start)

        
        
    

if __name__ == "__main__":
    unittest.main()