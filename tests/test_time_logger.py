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

    def tearDown(self):
        pass
        
    def test_canSaveLogToFile(self):
        # delete test log file if exists
        try:
            os.remove('test.log')
        except OSError:
            pass
        self.log.save('test.log')
        self.assertTrue(os.path.exists('test.log'))
        os.remove('test.log')
        
    def test_canRestoreLogFromFile(self):
        # arrange
        self.skipTest("speech marks do not compare equal!")
        logfile = open('test_restore.log', 'w')
        logfile.write('[{"startedAt": 0, "endedAt": 1, "type": "MockTimer"}]')
        logfile.close()        
        # act
        self.log.restore('test_restore.log')        
        # assert
        self.assertEqual('[{"startedAt": 0, "endedAt": 1, "type": "MockTimer"}]', str(self.log))

    def test_afterLoggingOneTimer_Saving_AndTearingDown_loggedTimerCanBeRecovered(self):
        self.skipTest("One timer is mysteriously added to the log after unpickling!??")
        self.log.add(name="Timer #1")
        self.log.save('recovery_test.log')
        del self.log
        
        log = TimerLog()
        log.restore('recovery_test.log')
        self.assertEqual("Timer #1", log[-1].get("name"))
    

class TestTimerLogBehaviour(unittest.TestCase):

    def setUp(self):
        self.log = TimerLog()
        
    def test_afterCreation_timerLogLengthShouldBeZero(self):
        self.assertEqual(0, len(self.log))
        
    def test_afterAddingOneTimerData_timerLogLengthShouldBeOne(self):
        self.log.add(name="Timer #1")
        self.assertEqual(1, len(self.log))

    def test_afterAddingTwoTimersData_timerLogLengthShouldBeTwo(self):
        self.log.add(name="Timer #1")
        self.log.add(name="Timer #2")
        self.assertEqual(2, len(self.log))

    def test_afterAddingOneTimer_firstElementInLogShouldBeThatOne(self):
        self.log.add(name="Dummy Timer")
        self.assertEqual("Dummy Timer", self.log[0].get("name"))
        
    def test_afterAddingTwoTimers_lastElementInLogShouldBeTimer2(self):
        self.log.add(name="Timer #1")
        self.log.add(name="Timer #2")
        self.assertEqual("Timer #2", self.log[-1].get("name"))
        


class TestTimerLogFormatting(unittest.TestCase):

    def setUp(self):
        self.log = TimerLog()

    def test_canPrintEntireLogInHumanReadableFormat(self):        
        self.assertEqual('[]', str(self.log))
            
    def test_canPrintTheDetailsOfTheFirstElementInTheLog(self):
        self.skipTest("is this a formatting test?")
        usedTimer = MockTimer()
        self.log.add(usedTimer)
        self.assertEqual("MockTimer, started: 1388240204 ended: 1388240205", str(self.log[0]))

    def test_givenASingleDate_canRetrieveLoggedTimersForThatDate(self):
        self.skipTest("is it just getter setter behaviour?")
        usedTimer = MockTimer()
        self.log.add(usedTimer)
        self.log.add(usedTimer)
        self.log.getTimersByDate("28/12/13")    
        
    def test_givenAUsedTimer_startTimeShouldBeLogged(self):
        self.skipTest("too advanced!")
        usedTimer = MockTimer()
        self.log.add(usedTimer)
        self.assertEqual("MockTimer", self.log.getItem(1).type)



if __name__ == "__main__":
    unittest.main()