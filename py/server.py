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
import cgi
import re
import wp

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import mwlib.htmlwriter
from mwlib import uparser

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
        print "getRawArticle: %s" % title

        # Retrieve article text, recursively following #redirects.
        while True:
            # Capitalize the first letter of the article -- Trac #6991.
            title = title[0].capitalize() + title[1:]
            # Replace underscores with spaces in title.
            title = title.replace("_", " ")
            article_text = wp.wp_load_article(title.encode('utf8'))
        
            # To see unmodified article_text, uncomment here.
            # print article_text

            m = re.match(r'^\s*\#?redirect\s*\[\[(.*)\]\]', article_text, re.IGNORECASE|re.MULTILINE)
            if not m: break
            title = m.group(1)
            
        article_text = unicode(article_text, 'utf8')
        return article_text

    def getTemplate(self, title, followRedirects=False):
        print "getTemplate: %s" % title
        return self.getRawArticle(title)

class WPImageDB:
    """Retrieves images for mwlib."""
    
    def hashpath(self, name):
        name = name.replace(' ', '_')
        name = name[:1].upper()+name[1:]
        d = md5(name.encode('utf-8')).hexdigest()
        return "/".join([d[0], d[:2], name])
    
    def getPath(self, name, size=None):
        hashed_name = self.hashpath(name)
        return 'images/%s' % hashed_name

    def getURL(self, name, size=None):
        hashed_name = self.hashpath(name)
        if os.path.exists('images/' + hashed_name):
            return '/images/' + hashed_name
        else:
            return 'http://upload.wikimedia.org/wikipedia/commons/' + hashed_name

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
        url = ("#".join([urllib.quote(x) for x in parts]))

        self.out.write("<a %s href='%s%s'>" % (link_attr, link_baseurl, url))

        if obj.children:
            for x in obj.children:
                self.write(x)
        else:
            self._write(obj.target)
        
        self.out.write("</a>")

class WikiRequestHandler(SimpleHTTPRequestHandler):
    @staticmethod
    def resolve_links(s, article_prelinks):
        # FIXME:  We do a substring search for each link to find out
        # whether an exact match exists in the local archive; if so,
        # we link internally.  We could probably save time with a 
        # C-level function that returns yes/no for "Is this exact
        # page title present in the index?"

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
    
    @staticmethod
    def strip_templates(wikitext):
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
        # Retrieve article text, recursively following #redirects.
        while True:
            # Capitalize the first letter of the article -- Trac #6991.
            title = title[0].capitalize() + title[1:]
            # Replace underscores with spaces in title.
            title = title.replace("_", " ")
            article_text = wp.wp_load_article(title)
        
            # To see unmodified article_text, uncomment here.
            # print article_text

            m = re.match(r'^\s*\#redirect\s+\[\[(.*)\]\]', article_text, re.IGNORECASE|re.MULTILINE)
            if not m: break
            title = m.group(1)
            
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
        article_text = WikiRequestHandler.resolve_links(self, article_text)

        # Remove any Wikitext templates as the JavaScript can't deal with these.
        # In the future, these should be evaluated when the database is built.
        article_text = WikiRequestHandler.strip_templates(article_text)
        
        # Embed article text and call parser.
        article_text = unicode(article_text, 'utf8')
        jstext = ''
        for l in article_text.split('\n'):
            jstext += re.escape(l) + '\\n\\\n'

        self.wfile.write("<script type='text/javascript'>");
        self.wfile.write("var wikitext = \"%s\";" % jstext.encode('utf8'));
        self.wfile.write("document.write(convert_wiki_to_html(unescape(wikitext)));");
        self.wfile.write("</script>")

    def send_wiki_html_mwlib(self, title, article_text):
        title = unicode(title, 'utf8')
        article_text = unicode(article_text, 'utf8')
        
        wikidb = WPWikiDB()
        imagedb = WPImageDB()
        
        parser = uparser.parseString(title, raw=article_text, wikidb=wikidb)
        
        writer = WPHTMLWriter(self.wfile, images=imagedb)
        writer.write(parser)

    def send_article(self, title):
        article_text = self.get_wikitext(title)
        
        # Redirect to Wikipedia if the article text is empty (e.g. an image link)
        if article_text == "":
            self.send_response(301)
            self.send_header("Location", 
                             "http://es.wikipedia.org/wiki/" + title)
            self.end_headers()
            return
    
        # Send HTTP header.
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
    
        # Write HTML header.
        self.wfile.write("<html><head><title>%s</title>" % title)
    
        # Embed CSS file.
        self.wfile.write("<style type='text/css' media='screen, projection'>"\
                         "@import '/static/monobook.css';</style>")
        
        self.wfile.write("</head>")
        
        # Write HTML body.
        self.wfile.write("<body>")
        
        # Convert wikitext to HTML and send.
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

        self.wfile.write("<html><head><title>Search Results for '%s'</title></head>" % title)

        # Embed CSS file.
        self.wfile.write("<style type='text/css' media='screen, projection'>"\
                         "@import '/static/monobook.css';</style>")

        self.wfile.write("</head>")

        self.wfile.write("<body>")
        
        self.wfile.write("<p>Search Results for '%s'.</p>" % title)
        self.wfile.write("<ul>")

        num_results = wp.wp_search(title)
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
            self.send_header("Location", redirect_url)
            self.end_headers()
            print "301 REDIRECT to '%s'" % redirect_url

    def do_GET(self):
        real_path = self.path
        real_path = urllib.url2pathname(real_path)

        (real_path, sep, param_text) = real_path.partition('?')
        self.params = {}
        for p in param_text.split('&'):
            (key, sep, value) = p.partition('=')
            self.params[key] = value

        m = re.match(r'^/(wiki|raw)/(.+)$', real_path)
        if m:
            self.send_article(m.group(2))
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
