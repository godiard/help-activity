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

import gtk

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolcombobox import ToolComboBox
from sugar._sugarext import AddressEntry

default_search_providers = {
    'schoolserver': {
        'order': 3,
        'name':  _('Wiki'),
        'url':   'http://localhost:8000/search?q=%s',
        'icon':  'zoom-home'
    },
}

class SearchToolbar(gtk.Toolbar):
    def __init__(self, activity):
        gtk.Toolbar.__init__(self)

        self._activity = activity        

        self._browser = self._activity._browser

        self._providercombo = ToolComboBox()

        self.insert(self._providercombo, -1)
        self._providercombo.show()

        self.set_providers(default_search_providers)
        
        self._entry = gtk.Entry()
        self._entry.connect('activate', self._entry_activate_cb)

        entry_item = gtk.ToolItem()
        entry_item.set_expand(True)
        entry_item.add(self._entry)
        self._entry.show()
        
        self.insert(entry_item, -1)
        entry_item.show()
  
    def _entry_activate_cb(self, entry):
        k = self._providercombo.combo.get_active_item()[0]
        p = self._providers[k]
        
        self._browser.load_uri(p['url'] % entry.props.text)
        self._browser.grab_focus()
        
        self._activity.toolbox.current_toolbar = 1

    def _cmp_provider_order(self, a, b):
        return self._providers[a]['order'] - self._providers[b]['order']
    
    def set_providers(self, providers):
        self._providers = providers
        
        self._providercombo.combo.remove_all()
        
        for k in sorted(self._providers.keys(), cmp=self._cmp_provider_order):
            p = self._providers[k]
            self._providercombo.combo.append_item(k, p['name'], p['icon'])
        
        self._providercombo.combo.set_active(0)
