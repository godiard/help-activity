#!/usr/bin/perl
# create a file recording the outgoing links for each page
# each line of the file represents a page and it's links,
# the first is the page name, all following are articles it links to
# inputs are page list and redirects list, and wikipedia snapshot as stdin, eg.:
# bzcat ../../eswiki-20080416-pages-articles.xml.bz2 |  ./PageLinks.pl top70k_pages all_redirects >| top70k_links
# NOTE - This program is slow to run. It's a little faster if you run with
# a smaller page list, so you don't bother assessing links for pages already excluded

use strict;
use warnings;

# input
my $pages = $ARGV[0];
my $redirects = $ARGV[1];

my %pagerank = ();
# read in pages as keys in a hash
open (PAGE,$pages);
while (<PAGE>) {
  chomp;
  $pagerank{$_} = 0;
}
close(PAGE);

my %redirects = ();
# read in redirects as key, value pairs in a hash
open (REDIR,$redirects);
while (<REDIR>) {
  if (/\[\[(.*?)\]\]\s*\[\[(.*?)\]\]/) {
    $redirects{$1} = $2;
  } else {
    die "redirects line is weird:\n$_\n";
  }
}
close(REDIR);

my $currpage = "";
my $intext = 0;
my $counter = 0;
while (<STDIN>) {
  if (/<title>(.*?)<\/title>/) {        # new page
    $counter++;
    $currpage = $1;
    if (exists $redirects{$currpage}) {
      next;
    } elsif (exists $pagerank{$currpage}) {
      $currpage =~ s/ /_/g;
      print "$currpage ";
    } else {
      next;
    }
    #if (0 == $counter % 100) {
    #  print "Working on ${counter}th page...\n";
    #}
    my $intext = 0;
    my $readmore = 1;
    my $pagetext = "";
    while ($readmore) {         # read in all page text at once
      if (/<text xml:space="preserve">(.*)/) {
        $intext = 1;
        $_ = $1;
      }
      if (/(.*)<\/text>/) {
        $intext = 0;
        $readmore = 0;
        $pagetext = $pagetext . $1;
      } elsif ($intext) {
        $pagetext = $pagetext . $_;
        if (length($pagetext) > 300000) {       # hack to hanging on ridiculously large pages
          #print "FAILPAGE! ";
          last;
        }
      }
      $_ = <STDIN>;
    }
    $pagetext =~ s/\n/ <newline> /g;            # to make sure we don't miss multi-line stuff
    $pagetext =~ s/(?<!=\[)\[([^\[\]]*?)\s*\](?!\])//g;  # remove all singleton brackets "links" so I can ignore them
    $pagetext =~ s/([^\[])\[([^\[])/$1$2/g;     # remove stranded left brackets
    $pagetext =~ s/([^\]])\]([^\]])/$1$2/g;     # remove stranded right brackets

    # now pull out each double bracketed object without brackets inside
    while ($pagetext =~ /^.*?\[\[\s*([^\[\]]*?)\s*\]\]/s) {
      my $match = $1;
      my $link = $match;
      if (not ($match =~ /^imagen?\W*:/i)) {    # check that it's not an image
        if ($match =~ /^:Categ/i) {             # remove preceding colon for category links
          $match =~ s/^:(Categ)/$1/;
        }
        if ($match =~ /^(.*?)\s*[#\|]/) {        # check for pipes or subsections and ignore
          $link = $1;
        }
        my $link = capitalize($link);
        if (exists $pagerank{$link}) {          # only print if it's a known page
          $link =~ s/ /_/g;
          print " $link";
        }
      }
      $pagetext =~ s/^(.*?)\[\[([^\[\]]*?)\s*\]\]/$1/s;  # remove this match from pagetext
    }
    print "\n";
  }
}

sub capitalize {
  my $word = shift;
  my $firstletter = substr($word,0,1);
  if ($firstletter =~ /[a-z]/) {
    my $newletter = uc($firstletter);
    substr($word,0,1) = $newletter;
  }
  # This is kind of a hack. I need to capitalize
  # the first letters when they're accented. - mad
  unless ($firstletter =~ /[a-zA-Z]/) {
    $firstletter = substr($word,0,2);
    if ($firstletter eq "á") {
      my $newletter = "Á";
      substr($word,0,2) = $newletter;
    } elsif ($firstletter eq "ñ") {
      my $newletter = "Ñ";
      substr($word,0,2) = $newletter;
    } elsif ($firstletter eq "é") {
      my $newletter = "É";
      substr($word,0,2) = $newletter;
    } elsif ($firstletter eq "ó") {
      my $newletter = "Ó";
      substr($word,0,2) = $newletter;
    }
  }
  #print "$word\n";
  return $word;
}
