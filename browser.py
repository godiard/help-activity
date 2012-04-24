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

from gi.repository import WebKit

_ZOOM_AMOUNT = 0.1


class Browser(WebKit.WebView):
    def __init__(self):
        WebKit.WebView.__init__(self)

    def do_setup(self):
        WebKit.WebView.do_setup(self)

    def zoom_in(self):
        # contentViewer = self.doc_shell.queryInterface( \
        #         interfaces.nsIDocShell).contentViewer
        # if contentViewer is not None:
        #     markupDocumentViewer = contentViewer.queryInterface( \
        #             interfaces.nsIMarkupDocumentViewer)
        #     markupDocumentViewer.fullZoom += _ZOOM_AMOUNT
        pass

    def zoom_out(self):
        # contentViewer = self.doc_shell.queryInterface( \
        #         interfaces.nsIDocShell).contentViewer
        # if contentViewer is not None:
        #     markupDocumentViewer = contentViewer.queryInterface( \
        #             interfaces.nsIMarkupDocumentViewer)
        #     markupDocumentViewer.fullZoom -= _ZOOM_AMOUNT
        pass
