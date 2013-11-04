import unittest
from rest_break import Break
from rest_break import AlreadySkippedError, CannotSkipOnceStarted, BreakAlreadyStarted
from time import sleep

class TestShortBreak(unittest.TestCase):

    def setUp(self):
        self.shortBreak = Break(self.whenTimeup)
                
    def whenTimeup(self):
        self.timeUp = True

    def assertRunning(self):
        return self.assertTrue(self.shortBreak.isRunning())

    def assertPostCondition_onceSkippedCanNeverBeRunning(self):
        return self.assertNotEqual(self.shortBreak.isRunning(), self.shortBreak.wasSkipped())    
    
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

    def test_afterStarting_BreakCallsBackWhenTimesUp(self):
        self.timeUp = False
        self.shortBreak = Break(self.whenTimeup, durationInMins=0.001)
        self.shortBreak.start()
        sleep(0.1)
        self.assertTrue(self.timeUp)
        
    def test_afterStarting_breakShouldNotCallBackBeforeTimesup(self):
        self.timeUp = False
        self.shortBreak = Break(self.whenTimeup, durationInMins=1)
        self.shortBreak.start()
        sleep(0.05)
        self.assertFalse(self.timeUp)

        
        
    

if __name__ == "__main__":
    unittest.main()