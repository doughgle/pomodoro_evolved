from mock import MagicMock, Mock
import jsonpickle

class MockTimerLog(MagicMock):
    
    def __init__(self, *args, **kw):
        MagicMock.__init__(self, *args, **kw)
        self.__str__ = Mock(return_value="Pomodoro started:  Sun 12/29/13 11:13:12 ended:  11:13:13")


class LoggedTimer(Mock):
    '''Pure and simple data structure.'''
    pass

    
class TimerLog(list):
    '''
    Persistent log of used Timers.
    '''

    def __init__(self):
        self._entire_formatted_log = ''
        super(TimerLog, self).__init__()
    
    def add(self, loggedTimer=None, name='undefined', startedAt=None, endedAt=None):
        loggedTimer = {'name': name}
        super(TimerLog, self).append(loggedTimer)
    
    def save(self, file_path):
        '''
        Saves this log to a given file path.
        '''
        logfile = open(file_path, 'w')
#        logfile.write(jsonpickle.encode(self, max_depth=2))
        print "before pickling= ", self
        pickled = jsonpickle.encode(self)
        print "pickled= ", pickled 
        logfile.write(pickled)
        logfile.close()

    def restore(self, file_path):
        logfile = open(file_path, 'r')
        self._entire_formatted_log = logfile.read()
        print "restored= ", self._entire_formatted_log
        unpickled = jsonpickle.decode(self._entire_formatted_log)        
        print "after unpickling= ", unpickled
        self.extend(unpickled)
        print "extended= ", self
        logfile.close()
