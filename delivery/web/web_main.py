#!/usr/bin/env python
import web
import os
import json
import time

urls = (
        '/', 'index',
        '/index.html', 'home',
        '/log/timer', 'LogTimer'
)

render = web.template.render('templates')

class index:
    
    def GET(self):
        return render.system_test()

class LogTimer(object):

    def __init__(self):
        pass
            
    def POST(self):
        log = open('timers.log', 'a')
        log_data = web.input()
        print(log_data.log)
        timer = json.loads(log_data.log)
        timer['loggedTime'] = time.strftime("%Y-%m-%dT%H:%M:%S")        
        log.write(json.dumps(timer) + os.linesep)
        log.close()
        
    def GET(self):
        return "Logging timer"


'''For development server use this code'''    
if __name__ == '__main__':
    app = web.application(urls, globals(), autoreload=True)
    app.run()

'''For deployment use this code'''
#application = web.application(urls, globals(), autoreload=False).wsgifunc()