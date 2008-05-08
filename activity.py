import os
import sys
import signal
import atexit

from sugar.activity import registry
activity_info = registry.get_registry().get_activity('org.laptop.WebActivity')

sys.path.append(activity_info.path)
import webactivity

# Default settings.
HTTP_PORT = '8000'
WIKIDB = '40ormore.xml.bz2'
HOME_PAGE = '/wiki/Peru'

# Activity class, extends WebActivity.
class WikipediaActivity(webactivity.WebActivity):
    def __init__(self, handle):
        
        print "Starting server...\n"
        
        os.chdir(os.environ['SUGAR_BUNDLE_PATH'])
        self.server_pid = os.spawnlp(os.P_NOWAIT, 'python', 'python', 'py/server.py', WIKIDB, HTTP_PORT)
        
        atexit.register(self.kill_server)
        
        handle.uri = 'http://localhost:%s%s' % (HTTP_PORT, HOME_PAGE)

        webactivity.WebActivity.__init__(self, handle)
    
    def kill_server(self):
        print "Stopping server...\n"
        os.kill(self.server_pid, signal.SIGHUP)
        