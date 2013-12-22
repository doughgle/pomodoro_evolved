import unittest
from rules_of_the_technique import RulesOfTheTechnique

class MockPomodoro(object):
    
    @property
    def type(self):
        return 'Pomodoro'
    
class MockShortBreak(object):
    
    @property
    def type(self):
        return "Short Break"
    
class MockLongBreak(object):
    
    @property
    def type(self):
        return "Long Break"
    

class TestRulesOfTheTechnique(unittest.TestCase):

    def setUp(self):
        self.rules = RulesOfTheTechnique(pomodoroCls=MockPomodoro, shortBreakCls=MockShortBreak, longBreakCls=MockLongBreak)        

    def assertPomodoro(self):
        return self.assertEqual("Pomodoro", self.timer.type)
    
    def assertShortBreak(self):
        return self.assertEqual("Short Break", self.timer.type)

    def assertLongBreak(self):
        return self.assertEqual("Long Break", self.timer.type)
        
    def test_startWithAPomodoro(self):
        self.timer = self.rules.newTimer()
        self.assertPomodoro()
                
    def test_afterOnePomodoro_takeAShortBreak(self):
        p = MockPomodoro()
        self.timer = self.rules.newTimer(prevTimer=p)
        self.assertShortBreak()
        
    def test_afterAShortBreak_doAPomodoro(self):
        sb = MockShortBreak()
        self.timer = self.rules.newTimer(prevTimer=sb)
        self.assertPomodoro()
        
    def test_afterFourPomodoros_takeALongBreak(self):
        for i in range(4):
            self.timer = self.rules.newTimer()
            self.assertPomodoro()
            self.timer = self.rules.newTimer(prevTimer=self.timer)
        self.assertLongBreak()


if __name__ == "__main__":
    unittest.main()
