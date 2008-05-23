#!/usr/bin/perl

use warnings;
use strict;

my $pagecounts = $ARGV[0];
my $threshold = $ARGV[1];
my $out = $ARGV[2];

my $outpages = $out . "_pages";
my $outlinks = $out . "_links";

open(IN,$pagecounts) or die "$pagecounts not available for reading!";
open(PAGES,">$outpages") or die "$outpages not available for writing!";


my @removepages = ("Wikipedia:","Ayuda:","Wikiproyecto:","MediaWiki:","Plantilla:","WP:","Portal:");

while (<IN>) {
  if (/(\d+).*\[\[(.*)\]\]/) {
    if ($1 > $threshold) {
      my $page = $2;
      my $good = 1;
      foreach my $remove (@removepages) {
        if ($page =~ /^$remove/) {
          $good = 0;
        }
      }
      if ($page eq "Portada") {
        $good = 0;
      }
      if ($good == 1) {
        print PAGES "$2\n";
      }
    }
  } else {
    die "WEIRD $_\n";
  }
}
close(IN);


