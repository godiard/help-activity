#!/usr/bin/perl

use URI::Escape;
use warnings;
use strict;


# using the traffic stats, get pagecounts for articles
# count pagecounts of redirect pages towards the main page,
# report counts for redirect as the counts of their main page

my $pagelist = $ARGV[0];
my $redirectlist = $ARGV[1];
my $trafficlist = $ARGV[2];

open(PAGES,$pagelist) or die;
my %pagecounts = ();
while (<PAGES>) {
  chomp;
  $pagecounts{$_} = 0;
}
close(PAGES);

#print "Done reading pages...\n";

open(REDIRECTS,$redirectlist) or die;
my %redirects = ();
while (<REDIRECTS>) {
  if (/\[\[(.*)\]\]\s*\[\[(.*)\]\]/) {
    $redirects{$1} = $2;
  }
}
close(REDIRECTS);

#print "Done reading redirects...\n";


open(TRAFFIC,$trafficlist) or die;
while (<TRAFFIC>) {
  my @data = split;
  my $page = $data[1];
  $page = uri_unescape($page);
  $page =~ s/_/ /g;
  if (exists $redirects{$page}) {
    if (exists $pagecounts{$redirects{$page}}) {
      $pagecounts{$redirects{$page}} += $data[2];
    }
  }
  if (exists $pagecounts{$page}) {
    $pagecounts{$page} += $data[2];
  } else {
    #print "$page doesn't exist on page list!\n";
  }
}

foreach my $page (keys %pagecounts) {
  if (exists $redirects{$page}) {
    if (exists $pagecounts{$redirects{$page}}) {
      print "$pagecounts{$redirects{$page}}\t[[$page]]\n";
    } else {
print "ERROR redirect page $page isn't on list??\n";
    }
  } elsif (exists $pagecounts{$page}) {
    print "$pagecounts{$page}\t[[$page]]\n";
  } else {
print "ERROR page $page not on list??\n";
  }
}

