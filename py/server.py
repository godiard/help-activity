#
# Web server script for Wikiserver project.
#
# Usage: server.py <dbfile> <port>
#
import sys
import os
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

parsers = [
    '/js/wiki2html.js',
    '/js/instaview-0.6.1.js',
    '/js/instaview-0.6.4.js',
    'mwlib',
]

default_parser = 3

class LinkStats:
    allhits = 1
    alltotal = 1
    pagehits = 1
    pagetotal = 1

class WPWikiDB:
    """Retrieves article contents for mwlib."""

    def getRawArticle(self, title):
        # Retrieve article text, recursively following #redirects.
        while True:
            # Capitalize the first letter of the article -- Trac #6991.
            title = title[0].capitalize() + title[1:]
            # Replace underscores with spaces in title.
            title = title.replace("_", " ")
            article_text = unicode(wp.wp_load_article(title.encode('utf8')), 'utf8')

            # To see unmodified article_text, uncomment here.
            # print article_text

            m = re.match(r'^\s*\#?redirect\s*\:?\s*\[\[(.*)\]\]', article_text, re.IGNORECASE|re.MULTILINE)
            if not m: break
            title = m.group(1)

        # WTB: Stripping whitespace improves template expansion.
        # TODO: Where is it coming from?
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
        hashed_name = self.hashpath(name)
        path = 'images/%s' % hashed_name
        #print "getPath: %s -> %s" % (name.encode('utf8'), path.encode('utf8'))
        return path

    def getURL(self, name, size=None):
        hashed_name = self.hashpath(name)
        if os.path.exists('images/' + hashed_name):
            url = '/images/' + hashed_name
        else:
            url = 'http://upload.wikimedia.org/wikipedia/commons/' + hashed_name
        #print "getUrl: %s -> %s" % (name.encode('utf8'), url.encode('utf8'))
        return url

class WPHTMLWriter(mwlib.htmlwriter.HTMLWriter):
    """Customizes HTML output from mwlib."""
    
    def __init__(self, wfile, images=None, math_renderer=None):
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
        article_exists = wp.wp_article_exists(title.encode('utf8'))
        
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

        if self.imglevel==0:
            self.imglevel += 1

            align = obj.align
            thumb = obj.thumb
            frame = obj.frame
            caption = obj.caption
            
            if re.match(r'.*\.svg$', url, re.IGNORECASE):
                tag = 'object data'
            else:
                tag = 'img src'
            
            print "writeImageLink url=%s frame=%s thumb=%s align=%s caption=%s width=%s" % \
                (url, frame, thumb, align, caption, width)
            
            attr = ''
            if width:
                attr += 'width="%d" ' % width
            
            img = '<%s="%s" %s longdesc="%s" %s/>' % (tag, url.encode('utf8'), caption.encode('utf8'), caption.encode('utf8'), attr);
            
            if thumb:
                frame = True
            
            center = False
            if align == 'center':
                center = True
                align = None
                
            if center:
                self.out.write('<div class="center">');

            if frame:
                if not align:
                    align = "right"
                self.out.write('<div class="thumb t%s">' % align)
                if thumb:
                    if not width:
                        width = 180 # default thumb width
        
                    self.out.write('<div style="width:%dpx;">' % (int(width)+2))
                    self.out.write(img)
                    self.out.write('<div class="thumbcaption">')
                    self.out.write('<div class="magnify" style="float:right">')
                    self.out.write('<a href="%s" class="internal" title="Enlarge">' % url.encode("utf8"))
                    self.out.write('<img src="/static/magnify-clip.png">')
                    self.out.write('</a>')
                    self.out.write('</div>')
                    for x in obj.children:
                        self.write(x)
                    self.out.write('</div>')
                    self.out.write('</div>')
                else:
                    self.out.write('<div>')
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

class WikiRequestHandler(SimpleHTTPRequestHandler):
    def resolve_links(self, article_prelinks):
        LinkStats.pagehits = 1
        LinkStats.pagetotal = 1

        for match in re.finditer(r"\[\[(.*?)\]\]", article_prelinks):
            if match:
                link = match.group(1)
                pipes = link.count("|")
                toreplace = "[[" + link + "]]"

                if pipes > 1:
                    continue

                # First, see if we have a [[foo|bar]]-style link.
                pipematch = re.search(r"(.*?)\|(.*)", link)

                if pipematch:
                    prepipe  = pipematch.group(1)
                    postpipe = pipematch.group(2)

                    title = prepipe
                    title = title[0].capitalize() + title[1:]
                    title = title.replace("_", " ")
                    article_exists = wp.wp_article_exists(title.encode('utf8'))

                    if article_exists:
                        # Exact match.  Internal link.
                        LinkStats.allhits += 1
                        LinkStats.alltotal += 1
                        LinkStats.pagehits += 1
                        LinkStats.pagetotal += 1
                        article_prelinks = article_prelinks.replace(toreplace, "<a href='/wiki/%s'>%s</a>" % (prepipe, postpipe))
                    else:
                        # No match.  External link.  Use es.wikipedia.org.
                        # FIXME:  Decide between es.w.o and schoolserver.
                        LinkStats.alltotal += 1
                        LinkStats.pagetotal += 1
                        article_prelinks = article_prelinks.replace(toreplace, "<a class='offsite' href='http://es.wikipedia.org/wiki/%s'>%s</a>" % (prepipe, postpipe))

                else:
                    # [[foo]]-style link.
                    title = link
                    title = title[0].capitalize() + title[1:]
                    title = title.replace("_", " ")
                    article_exists = wp.wp_article_exists(title.encode('utf8'))
                    
                    if article_exists:
                        LinkStats.allhits += 1
                        LinkStats.alltotal += 1
                        LinkStats.pagehits += 1
                        LinkStats.pagetotal += 1
                    else:
                        article_prelinks = article_prelinks.replace(toreplace, "<a class='offsite' href='http://es.wikipedia.org/wiki/%s'>%s</a>" % (link, link))
                        LinkStats.alltotal += 1
                        LinkStats.pagetotal += 1
                        
        return article_prelinks
    
    def strip_templates(self, wikitext):
        """Recursively strips all {{ }} style templates from 'wikitext'."""
        output = ''
        nest_level = 0
        i = 0
        while i < len(wikitext)-1:
            if wikitext[i] == '{' and wikitext[i+1] == '{':
                nest_level += 1
                i += 2
            elif wikitext[i] == '}' and wikitext[i+1] == '}':
                nest_level -= 1
                if nest_level < 0:
                    nest_level = 0
                i += 2
            else:
                if nest_level == 0:
                    output += wikitext[i]
                i += 1
        return output

    def get_wikitext(self, title):
        wikidb = WPWikiDB()
        article_text = wikidb.getRawArticle(title)
        
        # Pass ?noexpand=1 in the url to disable template expansion.
        if self.params.get('noexpand', 0):
            article_text = wikidb.getRawArticle(title)
            article_text = self.strip_templates(article_text)
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
    
    def send_wiki_html_js(self, article_text, parser):
        self.wfile.write("<script type='text/javascript' src='%s'></script>" % parser)

        #self.wfile.write("Internal hits on this page: %d<br>" % LinkStats.pagehits)
        #self.wfile.write("Total links on this page: %d<br>" % LinkStats.pagetotal)
        #page_percent = ((1.0 * LinkStats.pagehits / LinkStats.pagetotal) * 100)
        #self.wfile.write("Percentage: %.2f<br>" % page_percent)
        #self.wfile.write("Internal hits so far: %d<br>" % LinkStats.allhits)
        #self.wfile.write("Total links so far: %d<br>" % LinkStats.alltotal)
        #total_percent = ((1.0 * LinkStats.allhits / LinkStats.alltotal) * 100)
        #self.wfile.write("Percentage: %.2f<br>" % total_percent)        
        
        # Link resolution.
        article_text = self.resolve_links(article_text)

        # Embed article text and call parser.
        jstext = ''
        for l in article_text.split('\n'):
            jstext += re.escape(l) + '\\n\\\n'

        self.wfile.write("<script type='text/javascript'>");
        self.wfile.write("var wikitext = \"%s\";" % jstext.encode('utf8'));
        self.wfile.write("document.write(convert_wiki_to_html(unescape(wikitext)));");
        self.wfile.write("</script>")

    def send_wiki_html_mwlib(self, title, article_text):
        tokens = scanner.tokenize(article_text, title)

        wiki_parsed = parser.Parser(tokens, title).parse()
        wiki_parsed.caption = title

        imagedb = WPImageDB()
        writer = WPHTMLWriter(self.wfile, images=imagedb)
        writer.write(wiki_parsed)

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
        
            self.wfile.write("<style type='text/css' media='screen, projection'>"\
                             "@import '/static/common.css';"\
                             "@import '/static/monobook.css';"\
                             "@import '/static/styles.css';"\
                             "@import '/static/shared.css';"\
                             "</style>")
            
            self.wfile.write("</head>")
            
            self.wfile.write("<body>")
            
            parser_index = int(self.params.get('parser', default_parser))
            parser = parsers[parser_index]
            
            if parser == 'mwlib':
                self.send_wiki_html_mwlib(title, article_text)
            else:
                self.send_wiki_html_js(article_text, parser)
        
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
        if os.path.exists('images/' + path):
            # If image exists locally, serve it as normal.
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            # If not, redirect to wikimedia.
            redirect_url = "http://upload.wikimedia.org/wikipedia/commons/" + path
            self.send_response(301)
            self.send_header("Location", redirect_url.encode('utf8'))
            self.end_headers()

    def do_GET(self):
        real_path = urllib.unquote(self.path)
        real_path = unicode(real_path, 'utf8')

        (real_path, sep, param_text) = real_path.partition('?')
        self.params = {}
        for p in param_text.split('&'):
            (key, sep, value) = p.partition('=')
            self.params[key] = value

        m = re.match(r'^/wiki/(.+)$', real_path)
        if m:
            self.send_article(m.group(1))
            return

        m = re.match(r'^/search$', real_path)
        if m:
            self.send_searchresult(self.params.get('q', ''))
            return

        m = re.match(r'^/images/(.+)$', real_path)
        if m:
            self.send_image(m.group(1))
            return
        
        # Pass through all other requests to SimpleHTTPServer.
        SimpleHTTPRequestHandler.do_GET(self)

def load_db(dbname):
    wp.wp_load_dump(
        dbname + '.processed',
        dbname + '.locate.db',
        dbname + '.locate.prefixdb',
        dbname + '.blocks.db')

def run_server(port):
    httpd = BaseHTTPServer.HTTPServer(('', port), WikiRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    load_db(sys.argv[1])

    # This is an attempt to work around a race condition where Browse starts up before
    # the server has loaded the index.  Not working yet, though.
    #if os.fork():
    #    sys.exit(0)
        
    run_server(int(sys.argv[2]))
