import unittest
from rest_break import Break
from rest_break import BreakAlreadySkipped, CannotSkipOnceStarted
from rest_break import BreakAlreadyStarted, BreakNotStarted, BreakAlreadyTerminated
from time import sleep

class TestRestBreak(unittest.TestCase):

    def assertNotRunningNorSkipped(self):
        self.assertFalse(self.restBreak.isRunning())
        self.assertFalse(self.restBreak.wasSkipped())

    def setUp(self):
        self.restBreak = Break(self.whenTimeup)
                
    def whenTimeup(self):
        self.timeUp = True

    def assertRunning(self):
        return self.assertTrue(self.restBreak.isRunning())

    def assertPostCondition_onceSkippedCanNeverBeRunning(self):
        return self.assertNotEqual(self.restBreak.isRunning(), self.restBreak.wasSkipped())
    
    def test_afterCreationBreakIsNotRunning(self):
        self.assertFalse(self.restBreak.isRunning())
        
    def test_afterCreationBreakIsNotSkipped(self):
        self.assertFalse(self.restBreak.wasSkipped())
    
    def test_afterCreation_timeRemainingInSecondsIsEquivalentToDurationInMinutes(self):
        self.assertEqual((self.restBreak._durationInMins * 60), self.restBreak.timeRemaining)
            
    def test_afterSkipping_wasSkippedReturnsTrue(self):
        self.restBreak.skip()
        self.assertTrue(self.restBreak.wasSkipped())
        self.assertPostCondition_onceSkippedCanNeverBeRunning()
        
    def test_afterSkipping_startingABreakIsAnAlreadySkippedError(self):
        self.restBreak.skip()
        self.assertRaises(BreakAlreadySkipped, self.restBreak.start)
        self.assertPostCondition_onceSkippedCanNeverBeRunning()
    
    def test_afterStarting_isRunningReturnsTrue(self):
        self.restBreak.start()
        self.assertRunning()
        self.assertFalse(self.restBreak.wasSkipped())
        
    def test_afterStarting_skippingABreakIsACannotSkipBreakOnceStarted(self):
        self.restBreak.start()
        self.assertRaises(CannotSkipOnceStarted, self.restBreak.skip)
        
    def test_startingABreakThatIsAlreadyStartedIsAnAlreadyStartedException(self):
        self.restBreak.start()
        self.assertRaises(BreakAlreadyStarted, self.restBreak.start)

    def test_startingABreakAfterTimeup_isABreakTerminatedException(self):
        self.restBreak = Break(self.whenTimeup, durationInMins=0.001)
        self.restBreak.start()
        sleep(0.1)
        self.assertRaises(BreakAlreadyTerminated, self.restBreak.start)
        
    def test_startingABreakAfterStopped_isABreakTerminatedException(self):
        self.restBreak = Break(self.whenTimeup, durationInMins=0.001)
        self.restBreak.start()
        self.restBreak.stop()
        self.assertRaises(BreakAlreadyTerminated, self.restBreak.start)
        
    def test_afterStarting_BreakCallsBackWhenTimesUp(self):
        self.timeUp = False
        self.restBreak = Break(self.whenTimeup, durationInMins=0.001)
        self.restBreak.start()
        sleep(0.1)
        self.assertTrue(self.timeUp)
        
    def test_afterStarting_breakShouldNotCallBackBeforeTimesup(self):
        self.timeUp = False
        self.restBreak = Break(self.whenTimeup, durationInMins=1)
        self.restBreak.start()
        sleep(0.1)
        self.assertFalse(self.timeUp)
        
    def test_afterStarting_timeRemainingCanBeQueried(self):
        self.restBreak.start()
        sleep(1)
        self.assertEqual(299, self.restBreak.timeRemaining)
        
    def test_stoppingABreakThatsNotRunningIsABreakNotStartedError(self):
        self.assertRaises(BreakNotStarted, self.restBreak.stop)
        
    def test_stoppingABreakThatsSkipped_isABreakSkippedError(self):
        self.restBreak.skip()
        self.assertRaises(BreakAlreadySkipped, self.restBreak.stop)
        
    def test_afterStopping_breakWillNoLongerCallBack(self):
        self.timeUp = False
        self.restBreak = Break(self.whenTimeup, durationInMins=0.001)
        self.restBreak.start()
        self.restBreak.stop()
        sleep(0.1)
        self.assertFalse(self.timeUp)
        
    def test_afterStopping_breakIsNotRunningNorSkipped(self):
        self.restBreak.start()
        self.restBreak.stop()
        self.assertNotRunningNorSkipped()
                
    def test_afterTimeup_breakIsNotRunningNorSkipped(self):
        self.restBreak = Break(self.whenTimeup, durationInMins=0.001)
        self.restBreak.start()
        sleep(0.1)
        self.assertNotRunningNorSkipped()

    def test_afterTimeup_timeRemainingIsZero(self):
        self.restBreak = Break(self.whenTimeup, durationInMins=0.001)
        self.restBreak.start()
        sleep(0.1)
        self.assertEqual(0, self.restBreak.timeRemaining)
        
if __name__ == "__main__":
    unittest.main()
