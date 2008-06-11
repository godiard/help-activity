#!/usr/bin/perl

use strict;
use warnings;

# remove unlinked pages from a list of pages
# also remove any matching certain keywords
# input: page list, redirect list (from GetPages.pl)
# and page links (from PageLinks.pl)

my $pagelist = $ARGV[0];
my $redirectlist = $ARGV[1];
my $pagelinks = $ARGV[2];

# remove pages starting with these keywords
my @removepages = ("Wikipedia:","Ayuda:","Wikiproyecto:","MediaWiki:","Plantilla:","WP:","Portal:", "Categoría");

my %pagecounts = ();
open(PAGE,$pagelist) or die;
while(<PAGE>) {
  chomp;
  $pagecounts{$_} = 0;
}
close(PAGE);

my %redirects = ();
open(REDIR,$redirectlist) or die;
while (<REDIR>) {
  if (/\[\[(.*?)\]\]\s*\[\[(.*?)\]\]/) {
    $redirects{$1} = $2;
  } else {
    die "redirects line is weird:\n$_\n";
  }
}
close(REDIR);

open(LINKS,$pagelinks);
while (<LINKS>) {
  my @data = split;
  my $currpage = shift(@data);
  $currpage =~ s/_/ /g;
  unless (exists ($pagecounts{$currpage})) {
    next;
  }
  foreach my $link (@data) {
    $link =~ s/_/ /g;
    if (exists ($redirects{$link})) {
      if (exists ($pagecounts{$redirects{$link}})) {
        $pagecounts{$redirects{$link}}++;
      } else {
#print "Weird: $link redirects to $redirects{$link}, but this one isn't on the pagelist?\n";
      }
    }
    if (exists $pagecounts{$link}) {
      $pagecounts{$link}++;
    } else {
#print "$link does not exist on pagelist\n";
    }
  }
}

foreach my $page (keys %pagecounts) {
  my $good = 1;
  foreach my $remove (@removepages) {
    if ($page =~ /^$remove/) {
      $good = 0;
    }
  }
  if (($pagecounts{$page} >= 1) and $good) {
    print "$page\n";
  }
}
