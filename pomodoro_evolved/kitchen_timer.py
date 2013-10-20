'''
Copyright 2013 Douglas Hellinger

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from threading import Timer as TTimer
from time import time

class NotRunningError(Exception): pass
class AlreadyRunningError(Exception): pass


class Timer(object):
    
    running = "running"
    stopped = "stopped"
    timeup =  "timeup"
    
    def __init__(self):
        self.state = self.stopped        
        self.timeRemaining = 0
            
    def start(self, duration=1, whenTimeup=None):
        if self.state == self.running:
            raise AlreadyRunningError    
        else:
            self.timeRemaining = round(duration, 1)
            self._startTime = self._now()
            self._timer = TTimer(duration, self._whenTimeup)
            self._timer.start()            
            self.state = self.running            
            self._userWhenTimeup = whenTimeup
        
    def stop(self):
        if self.state == self.running:
            self.state = self.stopped
            self.timeRemaining -= round(self._elapsedTime(), 1)
        else:
            raise NotRunningError()
            
    def isTimeup(self):
        if self.state == self.timeup:
            return True
        else:
            return False
        
    def _whenTimeup(self):
        self.state = self.timeup
        self.timeRemaining = 0
        if callable(self._userWhenTimeup):
            self._userWhenTimeup()    
        
    def _now(self):
        return time()
    
    def _elapsedTime(self):
        return self._now() - self._startTime

