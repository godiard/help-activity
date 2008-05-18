# Copyright (C) 2007, One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gettext import gettext as _

import os
import sys
import signal
import atexit

from sugar.activity import registry
activity_info = registry.get_registry().get_activity('org.laptop.WebActivity')

sys.path.append(activity_info.path)
import webactivity

from searchtoolbar import SearchToolbar

# Default settings.
HTTP_PORT = '8000'
WIKIDB = 'mad_withtemplates.xml.bz2'
HOME_PAGE = '/static/index.html'

# Activity class, extends WebActivity.
class WikipediaActivity(webactivity.WebActivity):
    def __init__(self, handle):
        
        print "Starting server...\n"
        
        os.chdir(os.environ['SUGAR_BUNDLE_PATH'])
        self.server_pid = os.spawnlp(os.P_NOWAIT, 'python', 'python', 'py/server.py', WIKIDB, HTTP_PORT)
        
        atexit.register(self.kill_server)
        
        handle.uri = 'http://localhost:%s%s' % (HTTP_PORT, HOME_PAGE)

        webactivity.WebActivity.__init__(self, handle)
        
        self.searchtoolbar = SearchToolbar(self)
        self.toolbox.add_toolbar(_('Search'), self.searchtoolbar)
        self.searchtoolbar.show()    
    
    def kill_server(self):
        print "Stopping server...\n"
        os.kill(self.server_pid, signal.SIGHUP)

