#!/usr/bin/env python
import web
import os

urls = (
        '/', 'index',
        '/index.html', 'home',
        '/log/timer', 'log_timer'
)

render = web.template.render('templates')

class index:
    
    def GET(self):
        return render.system_test()

class log_timer(object):

    def __init__(self):
        pass
            
    def POST(self):
        log = open('timers.log', 'a')
        web_storage = web.input()
        timer_str = str(web_storage).rstrip('>').lstrip('<Storage ') + os.linesep
        print(timer_str)
        log.write(timer_str)
        log.close()
        
    def GET(self):
        return "Logging timer"


'''For development server use this code'''    
if __name__ == '__main__':
    app = web.application(urls, globals(), autoreload=True)
    app.run()

'''For deployment use this code'''
#application = web.application(urls, globals(), autoreload=False).wsgifunc()