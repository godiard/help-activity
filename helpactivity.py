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

import os
from gettext import gettext as _

import gtk
import gobject

from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton

import hulahop
hulahop.startup(os.path.join(activity.get_activity_root(), 'data/gecko'))

#from hulahop.webview import WebView
from browser import Browser
import xpcom
from xpcom.components import interfaces

gobject.threads_init()

HOME = os.path.join(activity.get_bundle_path(), 'help/XO_Introduction.html')
#HOME = "http://website.com/something.html"

class HelpActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.props.max_participants = 1

        self._web_view = Browser()

        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        toolbar = Toolbar(self._web_view)
        toolbox.add_toolbar(_('Navigation'), toolbar)
        toolbar.show()

        self.set_canvas(self._web_view)
        self._web_view.show()

        toolbox.set_current_toolbar(1)

        self._web_view.load_uri(HOME)

class Toolbar(gtk.Toolbar):
    def __init__(self, web_view):
        gobject.GObject.__init__(self)

        self._web_view = web_view

        self._back = ToolButton('go-previous-paired')
        self._back.set_tooltip(_('Back'))
        self._back.props.sensitive = False
        self._back.connect('clicked', self._go_back_cb)
        self.insert(self._back, -1)
        self._back.show()

        self._forward = ToolButton('go-next-paired')
        self._forward.set_tooltip(_('Forward'))
        self._forward.props.sensitive = False
        self._forward.connect('clicked', self._go_forward_cb)
        self.insert(self._forward, -1)
        self._forward.show()

        home = ToolButton('zoom-home')
        home.set_tooltip(_('Home'))
        home.connect('clicked', self._go_home_cb)
        self.insert(home, -1)
        home.show()

        progress_listener = self._web_view.progress
        progress_listener.connect('location-changed',
                                  self._location_changed_cb)
        progress_listener.connect('loading-stop', self._loading_stop_cb)

    def _location_changed_cb(self, progress_listener, uri):
        self.update_navigation_buttons()

    def _loading_stop_cb(self, progress_listener):
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        can_go_back = self._web_view.web_navigation.canGoBack
        self._back.props.sensitive = can_go_back

        can_go_forward = self._web_view.web_navigation.canGoForward
        self._forward.props.sensitive = can_go_forward

    def _go_back_cb(self, button):
        self._web_view.web_navigation.goBack()
    
    def _go_forward_cb(self, button):
        self._web_view.web_navigation.goForward()

    def _go_home_cb(self, button):
        self._web_view.load_uri(HOME)

