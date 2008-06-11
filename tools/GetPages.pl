#!/usr/bin/perl
# ./GetPages.pl
# Create list of pages and redirects for a wikipedia snapshot.
# Usage: Takes in a wikipedia snapshot as STDIN. First and second
# arguments give the "page list" and "redirect list" output locations.
# For example:
# bzcat ./eswiki-20080416-pages-articles.xml.bz2 | ./GetPages all_pages all_redirects

use strict;
use warnings;

my $pages = $ARGV[0];
my $redirects = $ARGV[1];

# open output files
open(PAGES,">$pages") or die;
open(REDIR,">$redirects") or die;

# Keep list of redirects as key, value hash pairs
my %redirects = ();
my $currpage = "";   # will store current page title
my $inpage = 0;
while (<STDIN>) {
  if (/<title>(.*?)<\/title>/) {   # start of new page!
    my $pagetitle = $1;
    $currpage = $1;
    print PAGES "$currpage\n";          # print page name to page list file
    $inpage = 0;                        # this should have been zeroed anyway...
  }
  if (/.*?<text xml.*?>(.*)/) {
    s/.*?<text xml.*?>//;
    $inpage = 1;        # keep track of when we've entered page text
  }
  if ((/#REDIRECT:?\s*\[\[\s*(.*?)\s*\]\]/i) and $inpage) {  # this is a redirect
    my $bracketed = $1;
    if ($bracketed =~ /:Categ/i) {
      $bracketed =~ s/:(Categ)/$1/i;
    }
    my $redirectpage = $bracketed;
    if ($bracketed =~ /(.*?)\s*[#\|]/) {
      $redirectpage = $1;
    }
    $redirectpage = capitalize($redirectpage);  # first of page names needs to be capitalized
    $redirectpage =~ s/_/ /g;                   # don't use underscores
    unless (exists $redirects{$currpage}) {
      # it turns out some pages have multiple redirects on them;
      # in wikipedia and in this program the first one listed "wins".
      $redirects{$currpage} = $redirectpage;
      print REDIR "[[$currpage]]\t[[$redirectpage]]\n";  # print redirect to redirect list file
    }
  } 
  if (/<\/text>/) {                             # out of text
    $inpage = 0;
  }
}

# capitalize: takes in a string, capitalizes the first letter
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
