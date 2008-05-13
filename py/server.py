#
# Web server script for Wikiserver project.
#
# Usage: server.py <dbfile> <port>
#
# TODO
#
# - Send content in the right charset.
# - Find a better way to locate instaview.js.
# + Make a nice looking page template, like the library.
# + Add a home page, like the library.
# - Use a style sheet.
# - Add a search box.
# - Return actual search results.
# + Instead of 404, send to home page.
# - Route non-cached and image links to schoolserver or wikipedia when available.
#
import sys
import os
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import urllib
import cgi
import re
import wp

parsers = [
    '/js/wiki2html.js',
    '/js/instaview-0.6.1.js',
    '/js/instaview-0.6.4.js',
]

default_parser = 2

class LinkStats:
    allhits = 1
    alltotal = 1
    pagehits = 1
    pagetotal = 1

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
                    lc_prepipe = prepipe.lower()
                    num_hits = wp.wp_search(lc_prepipe)

                    if num_hits > 0 and wp.wp_result(0).lower() == lc_prepipe:
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
                    lc_link = link.lower()
                    num_hits = wp.wp_search(lc_link)
                    if num_hits > 0 and wp.wp_result(0).lower() == lc_link:
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
            
    def send_article(self, title):
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

        # Remove any Wikitext templates as the JavaScript can't deal with these.
        # In the future, these should be evaluated when the database is built.
        article_text = WikiRequestHandler.strip_templates(article_text)

        # Link resolution.
        article_postlinks = WikiRequestHandler.resolve_links(self, article_text)
        article_text = unicode(article_postlinks, 'utf8')

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

        # Embed article source.
        parser_index = int(self.params.get('parser', default_parser))
        parser = parsers[parser_index]
        self.wfile.write("<script type='text/javascript' src='%s'></script>" % parser)

        #self.wfile.write("Internal hits on this page: %d<br>" % LinkStats.pagehits)
        #self.wfile.write("Total links on this page: %d<br>" % LinkStats.pagetotal)
        #page_percent = ((1.0 * LinkStats.pagehits / LinkStats.pagetotal) * 100)
        #self.wfile.write("Percentage: %.2f<br>" % page_percent)
        #self.wfile.write("Internal hits so far: %d<br>" % LinkStats.allhits)
        #self.wfile.write("Total links so far: %d<br>" % LinkStats.alltotal)
        #total_percent = ((1.0 * LinkStats.allhits / LinkStats.alltotal) * 100)
        #self.wfile.write("Percentage: %.2f<br>" % total_percent)        
        
        # Embed article text and call parser.
        jstext = ''
        for l in article_text.split('\n'):
            jstext += re.escape(l) + '\\n\\\n'

        self.wfile.write("<script type='text/javascript'>");
        self.wfile.write("var wikitext = \"%s\";" % jstext.encode('utf8'));
        self.wfile.write("document.write(convert_wiki_to_html(unescape(wikitext)));");
        self.wfile.write("</script>")
        
        self.wfile.write("</body></html>")

    def send_searchresult(self, title):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write("<html><head><title>Search Results for '%s'</title></head>" % title)
        self.wfile.write("<body>")
        
        self.wfile.write("<p>You asked for search term %s.</p>" % title)

        num_results = wp.wp_search(title)
        for i in xrange(0, num_results):
            result = unicode(wp.wp_result(i), 'utf8')
            self.wfile.write('<a href="/wiki/%s">%s</a><br>' %
                          (result.encode('utf8'), result.encode('utf8')))
            
        self.wfile.write("</body></html>")
    
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

    #if os.fork():
    #    sys.exit(0)
        
    run_server(int(sys.argv[2]))
