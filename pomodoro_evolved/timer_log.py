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
    
    def addTimer(self, loggedTimer=None, name='undefined', startedAt=None, endedAt=None):
        loggedTimer = {'name': name}
        super(TimerLog, self).append(loggedTimer)
    
    def save(self, file_path):
        '''
        Saves this log to a given file path.
        '''
        logfile = open(file_path, 'w')
        pickled = jsonpickle.encode(self)
        logfile.write(pickled)
        logfile.close()

    def restore(self, file_path):
        '''
        Restores log data from the given file path to this log.
        '''
        logfile = open(file_path, 'r')
        self._entire_formatted_log = logfile.read()
        unpickled = jsonpickle.decode(self._entire_formatted_log)
        self.extend(unpickled)
        logfile.close()
