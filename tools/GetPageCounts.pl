#!/usr/bin/perl

use URI::Escape;
use warnings;
use strict;

# using the traffic stats, get pagecounts for articles
# count pagecounts of redirect pages towards the main page,
# report counts for redirect as the counts of their main page

# page list and redirect list generated from GetPages.pl
my $pagelist = $ARGV[0];
my $redirectlist = $ARGV[1];
# traffic stats from file provided by Henrik
my $trafficlist = $ARGV[2];

# read in page list, store as keys in a "page counts" hash
# values initally zero, traffic numbers added to them
open(PAGES,$pagelist) or die;
my %pagecounts = ();
while (<PAGES>) {
  chomp;
  $pagecounts{$_} = 0;
}
close(PAGES);

# read in redirect list, store as hash key, value pairs
open(REDIRECTS,$redirectlist) or die;
my %redirects = ();
while (<REDIRECTS>) {
  if (/\[\[(.*)\]\]\s*\[\[(.*)\]\]/) {
    $redirects{$1} = $2;
  }
}
close(REDIRECTS);

# read traffic stats
open(TRAFFIC,$trafficlist) or die;
while (<TRAFFIC>) {
  my @data = split;
  my $page = $data[1];
  $page = uri_unescape($page);          # pages need to be unescaped
  $page =~ s/_/ /g;                     # and underscores converted
  if (exists $redirects{$page}) {                       # if redirect, also add count towards main page
    if (exists $pagecounts{$redirects{$page}}) {
      $pagecounts{$redirects{$page}} += $data[2];
    }
  }
  if (exists $pagecounts{$page}) {      # add count to this page
    $pagecounts{$page} += $data[2];
  } else {
    #print "$page doesn't exist on page list!\n";
  }
}

# now output traffic amounts, not ordered
foreach my $page (keys %pagecounts) {
  # If redirect, print target page's traffic score
  if (exists $redirects{$page}) {
    if (exists $pagecounts{$redirects{$page}}) {
      print "$pagecounts{$redirects{$page}}\t[[$page]]\n";
    } 
  } elsif (exists $pagecounts{$page}) {
    print "$pagecounts{$page}\t[[$page]]\n";
  }
}

