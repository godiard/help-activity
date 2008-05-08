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
# + Use a style sheet.
# + Add a search box.
# - Return actual search results.
# + Instead of 404, send to home page.
# + Route non-cached and image links to schoolserver or wikipedia when available.
#
import sys
import os
import BaseHTTPServer
import urllib
import cgi
import re
import wp

parsers = [
    'js/wiki2html.js',
    'js/instaview-0.6.1.js',
    'js/instaview-0.6.4.js',
]

default_parser = 2

class WikiRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def strip_templates(self, wikitext):
        """Recursively strips all {{{ }}} style templates from 'wikitext'."""
        output = ''
        nest_level = 0
        for c in wikitext:
            if c == '{':   nest_level += 1
            elif c == '}': nest_level -= 1
            elif nest_level <= 0: output += c
        return output
            
    def send_article(self, title):

        # Retrieve article text, recursively following #redirects.
        while True:
            article_text = wp.wp_load_article(title)
            m = re.match(r'^\s*\#redirect\s+\[\[(.*)\]\]', article_text, re.IGNORECASE|re.MULTILINE)
            if not m: break
            title = m.group(1)
        article_text = unicode(article_text, 'utf8')
        
        # Remove any Wikitext templates as the JavaScript can't deal with these.
        # In the future, these should be evaluated when the database is built.
        article_text = self.strip_templates(article_text)

        # Send HTTP header.
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # Write HTML header.
        self.wfile.write("<html><head><title>%s</title>" % title)

        # Embed CSS file.
        css_src = open('js/monobook.css').read()
        self.wfile.write("<style type='text/css' media='screen, projection'>%s</style>" % css_src)

        self.wfile.write("</head>")
        
        # Write HTML body.
        self.wfile.write("<body>")
        
        # Embed article source.
        parser_index = int(self.params.get('parser', default_parser))
        instaview_src = open(parsers[parser_index]).read()
        self.wfile.write("<script type='text/javascript'>%s</script>" % instaview_src)
        
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
        
        self.send_response(404)

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
