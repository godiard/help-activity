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
import json
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import WebKit

from sugar3.activity import activity
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

from viewtoolbar import ViewToolbar


def get_current_language():
    locale = os.environ.get('LANG')
    return locale.split('.')[0].split('_')[0].lower()


def get_index_uri():
    index_path = os.path.join(
        activity.get_bundle_path(),
        'html/%s/index.html' % get_current_language())

    if not os.path.isfile(index_path):
        index_path = os.path.join(
            activity.get_bundle_path(), 'html/index.html')
    return 'file://' + index_path


class HelpActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.props.max_participants = 1

        self._web_view = WebKit.WebView()
        self._web_view.set_full_content_zoom(True)

        _scrolled_window = Gtk.ScrolledWindow()
        _scrolled_window.add(self._web_view)
        _scrolled_window.show()

        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        viewtoolbar = ViewToolbar(self)
        viewbutton = ToolbarButton(page=viewtoolbar,
                                   icon_name='toolbar-view')
        toolbar_box.toolbar.insert(viewbutton, -1)
        viewbutton.show()

        separator = Gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        # lets reuse the code below
        navtoolbar = Toolbar(self._web_view)

        toolitem = Gtk.ToolItem()
        navtoolbar._home.reparent(toolitem)
        toolbar_box.toolbar.insert(toolitem, -1)
        navtoolbar._home.show()
        toolitem.show()

        toolitem = Gtk.ToolItem()
        navtoolbar._back.reparent(toolitem)
        toolbar_box.toolbar.insert(toolitem, -1)
        navtoolbar._back.show()
        toolitem.show()

        toolitem = Gtk.ToolItem()
        navtoolbar._forward.reparent(toolitem)
        toolbar_box.toolbar.insert(toolitem, -1)
        navtoolbar._forward.show()
        toolitem.show()

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        self.set_canvas(_scrolled_window)
        self._web_view.show()
        self._web_view.connect("resource-request-starting",
                               self._resource_request_starting_cb)
        self._web_view.load_uri(get_index_uri())

    def _resource_request_starting_cb(self, webview, web_frame, web_resource,
                                      request, response):
        uri = web_resource.get_uri()
        if uri.find('_images') > -1:
            if uri.find('/%s/_images/' % get_current_language()) > -1:
                new_uri = uri.replace('/html/%s/_images/' %
                                      get_current_language(),
                                      '/images/')
            else:
                new_uri = uri.replace('/html/_images/', '/images/')
            request.set_uri(new_uri)

    def get_document_path(self, async_cb, async_err_cb):
        html_uri = self._web_view.get_uri()
        rst_path = html_uri.replace('file:///', '/')
        rst_path = rst_path.replace('html/', 'source/')
        rst_path = rst_path.replace('.html', '.rst')
        tmp_path = os.path.join(activity.get_activity_root(), 'instance',
                                'source.rst')
        os.symlink(rst_path, tmp_path)
        async_cb(tmp_path)

    def read_file(self, file_path):
        f = open(file_path, "r")
        data = json.load(f)
        self._web_view.load_uri(data['current_page'])
        self._web_view.set_zoom_level(data['zoom_level'])
        f.close()

    def write_file(self, file_path):
        """
        Save the current uri, zoom level for load it in the next startup.
        """
        html_uri = self._web_view.get_uri()
        zoom_level = self._web_view.get_zoom_level()
        data = {'current_page': html_uri, 'zoom_level': zoom_level}

        f = open(file_path, "w")
        json.dump(data, f)
        f.close()


class Toolbar(Gtk.Toolbar):
    def __init__(self, web_view):
        GObject.GObject.__init__(self)

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

        self._web_view.connect('notify::uri', self._uri_changed_cb)

    def _uri_changed_cb(self, progress_listener, uri):
        self.update_navigation_buttons()

    def _loading_stop_cb(self, progress_listener):
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        self._back.props.sensitive = self._web_view.can_go_back()
        self._forward.props.sensitive = self._web_view.can_go_forward()

    def _go_back_cb(self, button):
        self._web_view.go_back()

    def _go_forward_cb(self, button):
        self._web_view.go_forward()

    def _go_home_cb(self, button):
        self._web_view.load_uri(get_index_uri())
