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
from viewtoolbar import ViewToolbar
gobject.threads_init()

HOME = os.path.join(activity.get_bundle_path(), 'help/XO_Introduction.html')
#HOME = "http://website.com/something.html"

class HelpActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.props.max_participants = 1

        self._web_view = Browser()

        try:
            from sugar.graphics.toolbarbox import ToolbarBox, ToolbarButton
            from sugar.activity.widgets import ActivityToolbarButton, StopButton, \
                                            ShareButton, KeepButton
            from mybutton import MyActivityToolbarButton

            toolbar_box = ToolbarBox()
            activity_button = MyActivityToolbarButton(self)
            toolbar_box.toolbar.insert(activity_button, 0)
            activity_button.show()

            viewtoolbar = ViewToolbar(self)
            viewbutton = ToolbarButton(page=viewtoolbar, \
                                        icon_name='camera')
            toolbar_box.toolbar.insert(viewbutton, -1)
            viewbutton.show()

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            toolbar_box.toolbar.insert(separator, -1)
            separator.show()

            #lets reuse the code below
            navtoolbar = Toolbar(self._web_view)
            navtoolbar._home.reparent(self)
            toolbar_box.toolbar.insert(navtoolbar._home, -1)
            navtoolbar._home.show()
            
            navtoolbar._back.reparent(self)
            toolbar_box.toolbar.insert(navtoolbar._back, -1)
            navtoolbar._back.show()
            
            navtoolbar._forward.reparent(self)
            toolbar_box.toolbar.insert(navtoolbar._forward, -1)
            navtoolbar._forward.show()

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            toolbar_box.toolbar.insert(separator, -1)
            separator.show()

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl><Shift>Q'
            toolbar_box.toolbar.insert(stop_button, -1)
            stop_button.show()

            self.set_toolbar_box(toolbar_box)
            toolbar_box.show()
            
        except ImportError:
            toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(toolbox)
            toolbox.show()

            toolbar = Toolbar(self._web_view)
            toolbox.add_toolbar(_('Navigation'), toolbar)
            toolbar.show()
            viewtoolbar = ViewToolbar(self)
            toolbox.add_toolbar(_('View'),viewtoolbar)
            viewtoolbar.show()

            toolbox.set_current_toolbar(1)
        
        self.set_canvas(self._web_view)
        self._web_view.show()

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

        self._home = ToolButton('go-home')
        self._home.set_tooltip(_('Home'))
        self._home.connect('clicked', self._go_home_cb)
        self.insert(self._home, -1)
        self._home.show()

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

