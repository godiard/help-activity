import os
import sys
import signal

from sugar.activity import activityfactory
from sugar.activity.registry import get_registry

import server

HTTP_PORT = 8000
WIKIDB = '40ormore.xml.bz2'
HOME_PAGE = '/wiki/Peru'

def start_server():
    server.run_server(HTTP_PORT)

def stop_server():
    sys.exit()

def start_browser():
    # FIXME:
    # Launching 'Web' in this way is problematic. It causes a second Browse
    # activity to appear in the home view, and leaves the Wikipedia
    # activity in the 'Starting...' state.
    #
    # A better solution might be to instantiate the Web activity class into
    # this process and spawn the server as a child process, rather than the
    # other way around.  In this case we will still need to use the
    # activityfactory to locate the Web activity bundle directory.
    activity = get_registry().find_activity('Web')[0]

    extra_args = ['-s', '-u', 'http://localhost:%d%s' % (HTTP_PORT, HOME_PAGE)]
    
    cmd_args = activityfactory.get_command(activity)
    cmd_args.extend(extra_args)

    os.execvpe(cmd_args[0], cmd_args, activityfactory.get_environment(activity))

def main():
    os.chdir(os.environ['SUGAR_BUNDLE_PATH'])

    server.load_db(WIKIDB)
    
    activity_pid = os.fork()

    if activity_pid:
        # Kill the server process when the browser process exits.
        def signal_sigchld(a, b):
            stop_server()
        signal.signal(signal.SIGCHLD, signal_sigchld)
        
        start_server()
        
    else:
        start_browser()

if __name__ == '__main__': main()
