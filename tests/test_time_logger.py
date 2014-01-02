import unittest
import os
from timer_log import TimerLog
      

class MockTimer(object):
    
    type = "MockTimer"
    
    def __str__(self):
        return "MockTimer, started: 1388240204 ended: 1388240205"


class TestTimerLogPersistence(unittest.TestCase):
    
    def setUp(self):
        self.log = TimerLog()
        
    def test_canSaveLogToFile(self):
        '''
        Tests that file will be created when TimerLog instance is saved.
        '''
        file_path = 'test_canSaveLogToFile.log'
        try:
            # delete test log file if exists
            os.remove(file_path)
        except OSError:
            pass
        self.log.save(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_afterLoggingOneTimer_Saving_AndTearingDown_loggedTimerCanBeRecovered(self):
        '''
        The timer log can be saved, deleted and then recovered from a file.
        This tests that the timer name can is recovered.
        '''
        file_path = 'test_afterLoggingOneTimer_Saving_AndTearingDown_loggedTimerCanBeRecovered.log'
        self.log.addTimer(name="Timer #1")
        self.log.save(file_path)
        del self.log
        log = TimerLog()
        log.restore(file_path)
        self.assertEqual("Timer #1", log[-1].get("name"))
    

class TestTimerLogAddAndRetrieveBehaviour(unittest.TestCase):

    def setUp(self):
        self.log = TimerLog()
        
    def test_afterCreation_timerLogLengthShouldBeZero(self):
        self.assertEqual(0, len(self.log))
        
    def test_afterAddingOneTimerData_timerLogLengthShouldBeOne(self):
        self.log.addTimer(name="Timer #1")
        self.assertEqual(1, len(self.log))

    def test_afterAddingTwoTimersData_timerLogLengthShouldBeTwo(self):
        self.log.addTimer(name="Timer #1")
        self.log.addTimer(name="Timer #2")
        self.assertEqual(2, len(self.log))

    def test_afterAddingOneTimer_firstElementInLogShouldBeThatOne(self):
        self.log.addTimer(name="Dummy Timer")
        self.assertEqual("Dummy Timer", self.log[0].get("name"))
        
    def test_afterAddingTwoTimers_lastElementInLogShouldBeTimer2(self):
        self.log.addTimer(name="Timer #1")
        self.log.addTimer(name="Timer #2")
        self.assertEqual("Timer #2", self.log[-1].get("name"))

    def test_givenASingleDate_canRetrieveLoggedTimersForThatDate(self):
        self.skipTest("is it just getter setter behaviour?")
        usedTimer = MockTimer()
        self.log.addTimer(usedTimer)
        self.log.addTimer(usedTimer)
        self.log.getTimersByDate("28/12/13")


class TestTimerLogFormatting(unittest.TestCase):

    def setUp(self):
        self.log = TimerLog()

    def test_canPrintEntireLogInHumanReadableFormat(self):
        self.assertEqual('[]', str(self.log))
            
    def test_canPrintTheDetailsOfTheFirstElementInTheLog(self):
        self.skipTest("is this a formatting test?")
        usedTimer = MockTimer()
        self.log.addTimer(usedTimer)
        self.assertEqual("MockTimer, started: 1388240204 ended: 1388240205", str(self.log[0]))


if __name__ == "__main__":
    unittest.main()
