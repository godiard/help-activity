#!/usr/bin/perl

use strict;
use warnings;

#my $input = $ARGV[0];
my $pages = $ARGV[0];
my $redirects = $ARGV[1];

my %pagerank = ();
# read in pages
open (PAGE,$pages);
while (<PAGE>) {
  chomp;
  $pagerank{$_} = 0;
}
close(PAGE);

my %redirects = ();
# read in redirects
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
  if (/<title>(.*?)<\/title>/) {
    $counter++;
    $currpage = $1;
    if (exists $redirects{$currpage}) {
      next;
    } else {
      $currpage =~ s/ /_/g;
      print "$currpage ";
    }
    #if (0 == $counter % 100) {
    #  print "Working on ${counter}th page...\n";
    #}
    my $intext = 0;
    my $readmore = 1;
    my $pagetext = "";
    while ($readmore) {
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
        if (length($pagetext) > 500000) {
print "FAILPAGE! ";
          last;
        }
      }
      $_ = <STDIN>;
    }
    # now $pagetext contains all of this page
    # process pagetext...
#print "pagetext:\n$pagetext\n";
    $pagetext =~ s/\n/ <newline> /g;
    $pagetext =~ s/(?<!=\[)\[([^\[\]]*?)\s*\](?!\])//g;  # remove all singleton brackets "links" so I can ignore them
    $pagetext =~ s/([^\[])\[([^\[])/$1$2/g;  # remove stranded left brackets
    $pagetext =~ s/([^\]])\]([^\]])/$1$2/g;  # remove stranded right brackets
#print "processed pagetext:\n$pagetext\n";

    while ($pagetext =~ /^.*?\[\[\s*([^\[\]]*?)\s*\]\]/s) {
      my $match = $1;
      #print "MATCH $match\n";
      my $link = $match;
      if (not ($match =~ /^imagen?\W*:/i)) {  # check that it's not an image
        if ($match =~ /^:Categ/i) {              # remove preceding colon for category links
          $match =~ s/^:(Categ)/$1/;
        }
        if ($match =~ /^(.*?)\s*[#\|]/) {        # check for pipes or subsections
          $link = $1;
        }
        my $link = capitalize($link);
        if (exists $pagerank{$link}) {
          $link =~ s/ /_/g;
          print " $link";
        }
      }
      $pagetext =~ s/^(.*?)\[\[([^\[\]]*?)\s*\]\]/$1/s;  # remove this match from pagetext
#      print "remaining pagetext:\n$pagetext\n";
    }
    print "\n";
  }
}

sub capitalize {
  my $word = shift;
  #print "$word to ";
  my $firstletter = substr($word,0,1);
  my $newletter = uc($firstletter);
  substr($word,0,1) = $newletter;
  #print "$word\n";
  return $word;
}
