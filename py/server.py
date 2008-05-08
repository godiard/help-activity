#
# Web server script for Wikiserver project.
#
# Usage: server.py <dbfile> <port>
#
# TODO
#
# + Send content in the right charset.
# + Find a better way to locate instaview.js.
# + Make a nice looking page template, like the library.
# + Add a home page, like the library.
# + Use a style sheet.
# + Add a search box.
# + Return actual search results.
# + Instead of 404, send to home page.
# + Route non-cached and image links to schoolserver or wikipedia when available.
#
import sys
import BaseHTTPServer
import urllib
import re
import wp

class WikiRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    @staticmethod
    def send_article(s, title):
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")
        s.end_headers()

        s.wfile.write("<html><head><title>%s</title></head>" % title)
        s.wfile.write("<body>")
        
        instaview_src = open('js/instaview.js').read()
        s.wfile.write("<script type='text/javascript'>%s</script>" % instaview_src)

        article_text = unicode(wp.wp_load_article(title), 'utf8')

        jstext = ''
        for l in article_text.split('\n'):
            jstext += re.escape(l) + '\\n\\\n'

        s.wfile.write("<script type='text/javascript'>");
        s.wfile.write("var wikitext = \"%s\";" % jstext.encode('utf8'));
        s.wfile.write("document.write(InstaView.convert(unescape(wikitext)));");
        s.wfile.write("</script>")
        
        s.wfile.write("</body></html>")

    @staticmethod
    def send_searchresult(s, title):
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")
        s.end_headers()

        s.wfile.write("<html><head><title>Search Results for '%s'</title></head>" % title)
        s.wfile.write("<body>")
        
        s.wfile.write("<p>You asked for search term %s.</p>" % title)
        
        s.wfile.write("</body></html>")
    
    def do_GET(s):
        real_path = s.path
        real_path = urllib.url2pathname(real_path)

        m = re.match(r'^/(wiki|raw)/(.+)$', real_path)
        if m:
            WikiRequestHandler.send_article(s, m.group(2))
            return
        
        m = re.match(r'^/search/(.+)$', real_path)
        if m:
            WikiRequestHandler.send_searchresult(s, m.group(1))
            return
        
        s.send_response(404)

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
    run_server(int(sys.argv[1]))
