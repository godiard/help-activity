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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

from sugar3.graphics.toolbutton import ToolButton


class ViewToolbar(Gtk.Toolbar):
    def __init__(self, activity):
        GObject.GObject.__init__(self)

        self._activity = activity

        self._browser = self._activity._web_view

        self.zoomout = ToolButton('zoom-out', accelerator='<ctrl>minus')
        self.zoomout.set_tooltip(_('Zoom out'))
        self.zoomout.connect('clicked', self.__zoomout_clicked_cb)
        self.insert(self.zoomout, -1)
        self.zoomout.show()

        self.zoomin = ToolButton('zoom-in', accelerator='<ctrl>plus')
        self.zoomin.set_tooltip(_('Zoom in'))
        self.zoomin.connect('clicked', self.__zoomin_clicked_cb)
        self.insert(self.zoomin, -1)
        self.zoomin.show()

        self.zoom_original = ToolButton('zoom-original', accelerator='<ctrl>0')
        self.zoom_original.set_tooltip(_('Actual size'))
        self.zoom_original.connect('clicked', self.__zoom_original_clicked_cb)
        self.insert(self.zoom_original, -1)
        self.zoom_original.show()

        self._zoom_update_sensitive()

        self.separator = Gtk.SeparatorToolItem()
        self.separator.set_draw(True)
        self.insert(self.separator, -1)
        self.separator.show()

        self.fullscreen = ToolButton('view-fullscreen')
        self.fullscreen.set_tooltip(_('Fullscreen'))
        self.fullscreen.connect('clicked', self.__fullscreen_clicked_cb)
        self.insert(self.fullscreen, -1)
        self.fullscreen.show()

    def _zoom_update_sensitive(self):
        self.zoomout.set_sensitive(self._activity.can_zoom_out())
        self.zoomin.set_sensitive(self._activity.can_zoom_in())
        self.zoom_original.set_sensitive(self._activity.can_zoom_original())

    def __zoomin_clicked_cb(self, button):
        if button.is_sensitive():
            self._activity.zoom_in()
        self._zoom_update_sensitive()

    def __zoomout_clicked_cb(self, button):
        if button.is_sensitive():
            self._activity.zoom_out()
        self._zoom_update_sensitive()

    def __zoom_original_clicked_cb(self, button):
        self._activity.zoom_original()
        self._zoom_update_sensitive()

    def __fullscreen_clicked_cb(self, button):
        self._activity.fullscreen()
