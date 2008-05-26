#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# 
# Web server script for Wikiserver project.
#
# Usage: server.py <dbfile> <port>
#
from __future__ import with_statement
import sys
import os
import codecs
from StringIO import StringIO
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import urllib
import re
import wp

# Uncomment to print out a large dump from the template expander.
#os.environ['DEBUG_EXPANDER'] = '1'

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import mwlib.htmlwriter
from mwlib import parser, scanner, expander

class LinkStats:
    allhits = 1
    alltotal = 1
    pagehits = 1
    pagetotal = 1

class ArticleIndex:
    # Prepare an in-memory index, using the already generated 
    # index file.  

    def __init__(self, path):
        self.article_index = set()
        with open(path, 'r') as f:
            for line in f.readlines():
                m = re.search(r'(.*?)\s*\d+$', line)
                if m is None:
                    raise AssertionError("Match didn't work")
                self.article_index.add(m.group(1))

    def __contains__(self, x):
        return x in self.article_index

class WPWikiDB:
    """Retrieves article contents for mwlib."""

    def getRawArticle(self, title):
        # Retrieve article text, recursively following #redirects.
        oldtitle = ""
        while True:
            # Replace underscores with spaces in title.
            title = title.replace("_", " ")
            # Capitalize the first letter of the article -- Trac #6991.
            title = title[0].capitalize() + title[1:]

            if title == oldtitle:
                article_text = ""
                break

            article_text = unicode(wp.wp_load_article(title.encode('utf8')), 'utf8')

            # To see unmodified article_text, uncomment here.
            # print article_text

            m = re.match(r'^\s*\#?redirect\s*\:?\s*\[\[(.*)\]\]', article_text, re.IGNORECASE|re.MULTILINE)
            if not m: break

            oldtitle = title
            title = m.group(1)

        # Stripping leading & trailing whitespace fixes template expansion.
        article_text = article_text.lstrip()
        article_text = article_text.rstrip()

        return article_text

    def getTemplate(self, title, followRedirects=False):
        return self.getRawArticle(title)

    def getExpandedArticle(self, title):
        article_text = self.getRawArticle(title)
        template_expander = expander.Expander(article_text, pagename=title, wikidb=self)
        article_text = template_expander.expandTemplates()
        return article_text

class WPImageDB:
    """Retrieves images for mwlib."""
    
    def hashpath(self, name):
        name = name.replace(' ', '_')
        name = name[:1].upper()+name[1:]
        d = md5(name.encode('utf-8')).hexdigest()
        return "/".join([d[0], d[:2], name])
    
    def getPath(self, name, size=None):
        hashed_name = self.hashpath(name).encode('utf8')
        path = 'es_PE/images/%s' % hashed_name
        #print "getPath: %s -> %s" % (name.encode('utf8'), path.encode('utf8'))
        return path

    def getURL(self, name, size=None):
        hashed_name = self.hashpath(name).encode('utf8')
        if os.path.exists('es_PE/images/' + hashed_name):
            url = '/es_PE/images/' + hashed_name
        else:
            url = 'http://upload.wikimedia.org/wikipedia/commons/' + hashed_name
        #print "getUrl: %s -> %s" % (name.encode('utf8'), url.encode('utf8'))
        return url

class HTMLOutputBuffer:
    """Buffers output and converts to utf8 as needed."""

    def __init__(self):
        self.buffer = ''

    def write(self, obj):
        if isinstance(obj, unicode):
            self.buffer += str(obj).encode('utf8')
        else:
            self.buffer += str(obj)
    
    def getvalue(self):
        return self.buffer
    
class WPHTMLWriter(mwlib.htmlwriter.HTMLWriter):
    """Customizes HTML output from mwlib."""
    
    def __init__(self, index, wfile, images=None, math_renderer=None):
        self.index = index
        self.gallerylevel = 0
        mwlib.htmlwriter.HTMLWriter.__init__(self, wfile, images, math_renderer)

    def writeLink(self, obj):
        if obj.target is None:
            return

        article = obj.target
        
        # Parser appending '/' characters to link targets for some reason.
        article = article.rstrip('/')
        
        title = article
        title = title[0].capitalize() + title[1:]
        title = title.replace("_", " ")

        article_exists = title.encode('utf8') in self.index
        
        if article_exists:
            # Exact match.  Internal link.
            LinkStats.allhits += 1
            LinkStats.alltotal += 1
            LinkStats.pagehits += 1
            LinkStats.pagetotal += 1
            link_attr = ''
            link_baseurl = '/wiki/'
        else:
            # No match.  External link.  Use es.wikipedia.org.
            # FIXME:  Decide between es.w.o and schoolserver.
            LinkStats.alltotal += 1
            LinkStats.pagetotal += 1
            link_attr = "class='offsite' "
            link_baseurl = "http://es.wikipedia.org/wiki/"

        parts = article.encode('utf-8').split('#')
        parts[0] = parts[0].replace(" ", "_")
        url = ("#".join([x for x in parts]))

        self.out.write("<a %s href='%s%s'>" % (link_attr, link_baseurl, url))

        if obj.children:
            for x in obj.children:
                self.write(x)
        else:
            self._write(obj.target)
        
        self.out.write("</a>")

    def writeImageLink(self, obj):
        if self.images is None:
            return

        width = obj.width
        height = obj.height

        if width and height:
            path = self.images.getPath(obj.target, size=max(width, height))
            url = self.images.getURL(obj.target, size=max(width, height))
        else:
            path = self.images.getPath(obj.target)
            url = self.images.getURL(obj.target)
            
        if url is None:
            return

        # The following HTML generation code is copied closely from InstaView, which seems to 
        # approximate the nest of <div> tags needed to render images close to right.
        # It's also been extended to support Gallery tags.
        if self.imglevel==0:
            self.imglevel += 1

            align = obj.align
            thumb = obj.thumb
            frame = obj.frame
            caption = obj.caption
            
            # SVG images must be included using <object data=''> rather than <img src=''>.
            if re.match(r'.*\.svg$', url, re.IGNORECASE):
                tag = 'object'
                ref = 'data'
            else:
                tag = 'img'
                ref = 'src'
            
            # Hack to get galleries to look okay, in the absence of image dimensions.
            if self.gallerylevel > 0:
                width = 120
            
            if thumb and not width:
                width = 180 #FIXME: This should not be hardcoded
    
            attr = ''
            if width:
                attr += 'width="%d" ' % width
            
            img = '<%(tag)s %(ref)s="%(url)s" longdesc="%(caption)s" %(attr)s></%(tag)s>' % \
               {'tag':tag, 'ref':ref, 'url':url, 'caption':caption, 'attr':attr}
            
            center = False
            if align == 'center':
                center = True
                align = None

            if center:
                self.out.write('<div class="center">');

            if self.gallerylevel > 0:
                self.out.write('<div class="gallerybox" style="width: 155px;">')
                
                self.out.write('<div class="thumb" style="padding: 13px 0; width: 150px;">')
                self.out.write('<div style="margin-left: auto; margin-right: auto; width: 120px;">')
                self.out.write('<a href="%s" class="image" title="%s">' % (url, caption))
                self.out.write(img)
                self.out.write('</a>')
                self.out.write('</div>')
                self.out.write('</div>')

                self.out.write('<div class="gallerytext">')
                self.out.write('<p>')
                for x in obj.children:
                    self.write(x)
                self.out.write('</p>')
                self.out.write('</div>')

                self.out.write('</div>')
            elif frame or thumb:
                if not align:
                    align = "right"
                self.out.write('<div class="thumb t%s">' % align)

                if not width:
                    width = 180 # default thumb width
                self.out.write('<div style="width:%dpx;">' % (int(width)+2))

                if thumb:
                    self.out.write(img)
                    self.out.write('<div class="thumbcaption">')
                    self.out.write('<div class="magnify" style="float:right">')
                    self.out.write('<a href="%s" class="internal" title="Enlarge">' % url)
                    self.out.write('<img src="/static/magnify-clip.png">')
                    self.out.write('</a>')
                    self.out.write('</div>')
                    for x in obj.children:
                        self.write(x)
                    self.out.write('</div>')
                else:
                    self.out.write(img)
                    self.out.write('<div class="thumbcaption">')
                    for x in obj.children:
                        self.write(x)
                    self.out.write('</div>')

                self.out.write('</div>')
                self.out.write('</div>')
            elif align:
                self.out.write('<div class="float%s">' % align)
                self.out.write(img)
                self.out.write('</div>')
            else:
                self.out.write(img)

            if center:
                self.out.write('</div>');

            self.imglevel -= 1
        else:
            self.out.write('<a href="%s">' % url.encode('utf8'))
            
            for x in obj.children:
                self.write(x)
                
            self.out.write('</a>')

    def writeTagNode(self, t):
        if t.caption == 'gallery':
            self.out.write('<table class="gallery"  cellspacing="0" cellpadding="0">')
            
            self.gallerylevel += 1

            # TODO: More than one row.
            self.out.write('<tr>')
            
            for x in t.children:
                self.out.write('<td>')
                self.write(x)
                self.out.write('</td>')
                
            self.out.write('</tr>')

            self.gallerylevel -= 1
            
            self.out.write('</table>')
        else:
            # All others handled by base class.
            mwlib.htmlwriter.HTMLWriter.writeTagNode(self, t)

class WikiRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, index, request, client_address, server):
        self.index = index
        self.client_address = client_address
        SimpleHTTPRequestHandler.__init__(
            self, request, client_address, server)

    def get_wikitext(self, title):
        wikidb = WPWikiDB()
        article_text = wikidb.getRawArticle(title)
        
        # Pass ?noexpand=1 in the url to disable template expansion.
        if self.params.get('noexpand', 0):
            article_text = wikidb.getRawArticle(title)
        else:
            article_text = wikidb.getExpandedArticle(title)

        # Pass ?override=1 in the url to replace wikitext for testing the renderer.
        if self.params.get('override', 0):
            try:
                override = open('override.txt', 'r')
                article_text = unicode(override.read(), 'utf8')
                override.close()
            except:
                pass

        return article_text
    
    def send_wiki_html(self, title, article_text):
        tokens = scanner.tokenize(article_text, title)

        wiki_parsed = parser.Parser(tokens, title).parse()
        wiki_parsed.caption = title

        htmlbuf = HTMLOutputBuffer()
        
        imagedb = WPImageDB()
        writer = WPHTMLWriter(self.index, htmlbuf, images=imagedb)
        writer.write(wiki_parsed)
        
        self.wfile.write(htmlbuf.getvalue())

    def send_article(self, title):
        article_text = self.get_wikitext(title)

        # Capitalize the first letter of the article -- Trac #6991.
        title = title[0].capitalize() + title[1:]

        # Replace underscores with spaces in title.
        title = title.replace("_", " ")

        # Redirect to Wikipedia if the article text is empty (e.g. an image link)
        if article_text == "":
            self.send_response(301)
            self.send_header("Location", 
                             "http://es.wikipedia.org/wiki/" + title.encode('utf8'))
            self.end_headers()
            return

        # Pass ?raw=1 in the URL to see the raw wikitext (post expansion, unless noexpand=1 is also set).
        if self.params.get('raw', 0):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
        
            self.wfile.write(article_text.encode('utf8'))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
        
            self.wfile.write("<html><head><title>%s</title>" % title.encode('utf8'))
        
            self.wfile.write("<style type='text/css' media='screen, projection'>"
                             "@import '/static/common.css';"\
                             "@import '/static/monobook.css';"\
                             "@import '/static/styles.css';"\
                             "@import '/static/shared.css';"\
                             "</style>")
            
            self.wfile.write("</head>")
            
            self.wfile.write("<body>")
            
            self.send_wiki_html(title, article_text)

            self.wfile.write('<center>Contenido disponible bajo los términos de la <a href="/static/es-gfdl.html">Licencia de documentación libre de GNU</a>. <br/> Wikipedia es una marca registrada de la organización sin ánimo de lucro Wikimedia Foundation, Inc.<br/><a href="/static/acerca.html">Acerca de Wikipedia</a> </center>')
            self.wfile.write("</body></html>")
    
    def send_searchresult(self, title):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write("<html><head><title>Search Results for '%s'</title></head>" % title.encode('utf8'))

        self.wfile.write("<style type='text/css' media='screen, projection'>"\
                         "@import '/static/monobook.css';</style>")

        self.wfile.write("</head>")

        self.wfile.write("<body>")
        
        self.wfile.write("<h1>Search Results for '%s'.</h1>" % title.encode('utf8'))
        self.wfile.write("<ul>")

        num_results = wp.wp_search(title.encode('utf8'))
        for i in xrange(0, num_results):
            result = unicode(wp.wp_result(i), 'utf8')
            self.wfile.write('<li><a href="/wiki/%s">%s</a></li>' %
                          (result.encode('utf8'), result.encode('utf8')))

        self.wfile.write("</ul>")
            
        self.wfile.write("</body></html>")

    def send_image(self, path):
        if os.path.exists('es_PE/images/' + path.encode('utf8')):
            # If image exists locally, serve it as normal.
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            # If not, redirect to wikimedia.
            redirect_url = "http://upload.wikimedia.org/wikipedia/commons/%s" \
                         % path.encode('utf8')
            self.send_response(301)
            self.send_header("Location", redirect_url.encode('utf8'))
            self.end_headers()

    def handle_feedback(self, feedtype, article):
        with codecs.open("feedback.log", "a", "utf-8") as f:
           f.write(feedtype +"\t"+ article +"\t" + self.client_address[0] +"\n")
           f.close()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        if feedtype == "render":
            strtype = "un error de presentación"
        elif feedtype == "report":
            strtype = "material inapropriado"

        self.wfile.write("<html><title>Comentario recibido</title>Gracias por reportar %s en la pagina <b>%s</b>.</html>" % (strtype, article.encode('utf8')))

    def do_GET(self):
        real_path = urllib.unquote(self.path)
        real_path = unicode(real_path, 'utf8')

        (real_path, sep, param_text) = real_path.partition('?')
        self.params = {}
        for p in param_text.split('&'):
            (key, sep, value) = p.partition('=')
            self.params[key] = value

        # Wiki requests return article contents or redirect to Wikipedia.
        m = re.match(r'^/wiki/(.+)$', real_path)
        if m:
            self.send_article(m.group(1))
            return

        # Search requests return search results.
        m = re.match(r'^/search$', real_path)
        if m:
            self.send_searchresult(self.params.get('q', ''))
            return

        # Image requests are handled locally or are referenced from Wikipedia.
        m = re.match(r'^/es_PE/images/(.+)$', real_path)
        if m:
            self.send_image(m.group(1))
            return

        # Static requests handed off to SimpleHTTPServer.
        m = re.match(r'^/static/(.*)$', real_path)
        if m:
            SimpleHTTPRequestHandler.do_GET(self)
            return

        # Feedback links.
        m = re.match(r'^/(report|render)$', real_path)
        if m:
            self.handle_feedback(m.group(1), self.params.get('q', ''))
            return

        # Any other request redirects to the index page.        
        self.send_response(301)
        self.send_header("Location", "/static/")
        self.end_headers()

def load_db(dbname):
    wp.wp_load_dump(
        dbname + '.processed',
        dbname + '.locate.db',
        dbname + '.locate.prefixdb',
        dbname + '.blocks.db')

def run_server(path, port):
    index = ArticleIndex('%s.index.txt' % path)

    httpd = BaseHTTPServer.HTTPServer(('', port),
        lambda *args: WikiRequestHandler(index, *args))

    from threading import Thread
    server = Thread(target=httpd.serve_forever)
    server.start()
    #httpd.serve_forever()
    
    # Tell the world that we're ready to accept request.
    print 'ready'


if __name__ == '__main__':
    load_db(sys.argv[1])

    run_server(sys.argv[1], int(sys.argv[2]))
