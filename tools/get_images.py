from __future__ import with_statement
import re
#import server
import md5
import urllib
import collections
import os
import subprocess

BASEWORD = r"Image"

BASE_URL="http://upload.wikimedia.org/wikipedia/commons"

def get_source_url(filename):
    return "%s/%s" % (BASE_URL, get_endpath(filename))

def get_dirs(filename):
    m = md5.new()
    m.update(filename)
    h = m.hexdigest()
    return (h[0], h[:2])

def get_endpath(filename):
    d = get_dirs(filename)
    p = "%s/%s/%s" % (d[0], d[1], filename)
    return p

def canonicalize_filename(wikiname):
    wikiname = wikiname.replace(' ', '_')
    wikiname = wikiname[0].upper() + wikiname[1:]
    return wikiname

class WorkaroundURLopener(urllib.FancyURLopener):
    version = "OLPC_wikislicer/0.1"

urllib._urlopener = WorkaroundURLopener()

def download_image(filename, base_dir):
    source = get_source_url(filename)
    dirs = get_dirs(filename)
    destdir = "%s/%s/%s" % (base_dir, dirs[0], dirs[1])
    try:
        os.makedirs(destdir)
    except:
        pass #This just means that destdir already exists
    dest = "%s/%s" % (destdir, filename)
    try:
        urllib.urlretrieve(source,dest)
    except:
        print "Failed to download " + source
        return False
    return dest

def make_svg_wrapper(name, width, height):
    s = '<svg xmlns="http://www.w3.org/2000/svg" version="1.2" xmlns:xlink="http://www.w3.org/1999/xlink" width="%(width)i" height="%(height)i" viewbox="0 0 %(width)i %(height)i"><image xlink:href="%(name)s" width="100%%" height="100%%" x="0" y="0"/></svg>' % {'name':name, 'width':width, 'height':height }
    return s

def get_dims(path):
    try:
        p = subprocess.Popen(['identify','-format','%wx%h',path],stdout=subprocess.PIPE)
        p.wait()
        s = p.stdout.read()
        l = s.split('x')
        return (int(l[0]), int(l[1]))
    except:
        print "Failed to get dims"
        return False

def download_and_process(imgdict, base_dir, thumb_width):
    for wikiname in imgdict:
        filename = canonicalize_filename(wikiname)
        d = download_image(filename, base_dir)
        if d:
            width = None
            height= None
            for p in imgdict[wikiname]:
                if p.width is not None:
                    width = max(width, p.width)
                elif p.thumbnail:
                    width = max(width, thumb_width)
                if p.height is not None:
                    height = max(height, p.height)
            process_image(filename, width, height)

MAXWIDTH=800
MAXHEIGHT=800
def process_image(d, width=None, height=None):
        vector = d[-3:].upper() == 'SVG'
        if vector:
            try:
                jpg_name = d + '.jpg'
                rsvg_command = ['rsvg-convert','--keep-aspect-ratio','--format=png','--output', jpg_name]
                if width is not None:
                    rsvg_command.append('--width=%i' % width)
                if height is not None:
                    rsvg_command.append('--height=%i' %height)
                rsvg_command.append(d)
                subprocess.check_call(rsvg_command)
                #jpg_name file now contains a png image; we want jpg to save space
                subprocess.check_call(['convert', "PNG:%s" % jpg_name, "-quality", "20", "JPEG:%s" % jpg_name])
                (width, height) = get_dims(jpg_name)

                svg_factor = 0.3 #favorability of SVG
                print "Processing vector image " + d
                jpg_size = os.stat(jpg_name).st_size 
                svg_size = svg_factor * os.stat(d).st_size
                if svg_size > jpg_size: 
                    print "Replacing svg by a raster wrapper"
                    endname = jpg_name.split('/')[-1]
                    s = make_svg_wrapper(endname, width, height)
                    f = open(d,'w')
                    f.write(s)
                    f.truncate()
                    f.close()
                    return jpg_size + os.stat(d).st_size
                else:
                    print "Preserving svg as vector"
                    os.remove(jpg_name)
                    return os.stat(d).st_size
            except:
                print "Error: convert failed on " + d
                try:
                    os.remove(d)
                    os.remove(jpg_name)
                except:
                    print "Error: failed to remove " + d
                return 0
                
        else:
            print "Processing raster image " + d
            try:
                if width is None:
                    width = MAXWIDTH
                if height is None:
                    height = MAXHEIGHT
                newsize = "%ix%i>" % (width, height)
                subprocess.check_call(['convert', d,"-flatten", "-resize", newsize, "-quality", "20", "JPEG:%s" % d])
                print "Succesfully resized " + d
                return os.stat(d).st_size
            except:
                print "Error: convert failed on " + d
                try:
                    os.remove(d)
                except:
                    print "Error: failed to remove " + d
                return 0

def process_imagelist(list_filename, base_dir, imgword, maxsize=float('inf')):
    with open(list_filename) as f:
        print "opened " + list_filename
        totalsize = 0 #bytes
        searcher = r"\[\[(?:%s|%s):(.+?)\]\]\s+(\d+)\s+(.*?)\s+(.*?)$" % (BASEWORD, imgword)
        print searcher
        for line in f.readlines():
            m = re.search(searcher, line)
            if m is None:
                print "WARNING: Match didn't work on " + line
            wikiname = m.group(1)
            hits = m.group(2)
            width = m.group(3)
            height = m.group(4)
            print wikiname, hits, width, height
            
            if width == 'None':
                width = None
            else:
                width = int(width)
            
            if height == 'None':
                height = None
            else:
                height = int(height)
    
            filename = canonicalize_filename(wikiname)
            d = download_image(filename, base_dir)
            if d:
                s = process_image(d, width, height)
                totalsize += s
                print d + " occupies " + str(s)  + " bytes; running total is " + str(totalsize)
                if totalsize > maxsize:
                    break

class ImageProps:
    thumbnail = False
    width = None
    height = None
    upright = False

    def __repr__(self):
        return "%s (%s, %s) %s" % (self.thumbnail, self.width, self.height, self.upright)

class ImageFinder:
    def __init__(self, image_word):
        self.word = image_word
        self.db = server.WPWikiDB()

    def find_images(self, text):
        L = []
        
        #pattern = r"\[\[(?:%s|%s):(?P<filename>[^\|\]]+)(?:\|(?P<type>thumb|thumbnail)|(?P<width>\d+)(?:x(?P<height>\d+))?px|(?P<upright>upright)|(?:[^\|\[\]]|\[[^\|\[\]]*\]|\[\[[^\|\[\]]*\]\])*)*\]\]" % (BASEWORD, self.word)
        #pattern = r"\[\[(?:%s|%s):(?P<filename>[^\|\]]+)(?P<options>(?:[^\[\]]|\[[^\[\]]*\]|\[\[[^\[\]]*\]\])*)\]\]" % (BASEWORD, self.word)
        pattern = r"\[\[(?:%s|%s):\s*(?P<filename>[^\|\]]+?)\s*(?:\|(?P<options>(?:[^\[\]]|\[[^\[\]]*\]|\[\[[^\[\]]*\]\])*))?\]\]" % (BASEWORD, self.word)
        for match in re.finditer(pattern, text):
            if match:
                #d = match.groupdict(None)
                f = match.group('filename')
                p = ImageProps()
                for s in match.group('options').split('|'):
                    if s == 'thumb' or s == 'thumbnail':
                        p.thumbnail = True
                    elif s == 'upright':
                        p.upright = False
                    elif s[-2:] == 'px':
                        dims = s[:-2].split('x')
                        if len(dims) > 0:
                            p.width = int(dims[0])
                        if len(dims) > 1:
                            p.height = int(dims[1])
                print (f,p)
                L.append((f,p))
        return L

    def get_images_info(self, title):
        text = self.db.getExpandedArticle(title)
        return self.find_images(text)

    def list_images(self, title):
        props = self.get_images_info(title)
        filenames = [t[0] for t in props]
        return filenames

    def get_metadata_all(self, titles):
        d = collections.defaultdict(list)
        for t in titles:
            L = self.get_images_info(t)
            for (fname, props) in L:
                d[fname].append(props)
        return d

def read_links(index):
    f = open(index)
    text = f.read()
    f.close()
    titles = []
    for match in re.finditer('href\s*=\s*[\'\"]/wiki/([^\'\"]+)[\'\"]', text):
        if match:
            titles.append(match.group(1))
    return titles

def main_task(db_path, indexfile, image_word, base_dir, thumb_width):
    titles = read_links(indexfile)
    print titles
    server.load_db(db_path)
    p = ImageFinder(image_word)
    m = p.get_metadata_all(titles)
    print m
    download_and_process(m, base_dir, thumb_width)

#main_task("/home/olpc/40ormore.xml.bz2", "../static/index.html", "Imagen", "/home/olpc/images", 180)
process_imagelist("top70k_images", "../es_PE/images", "Imagen", 23000000)
