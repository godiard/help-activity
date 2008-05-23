#!/usr/bin/perl

use strict;
use warnings;

my $BASEMULT = 6;

my $pageranks = $ARGV[0];
my $basepages = $ARGV[1];
my $imagerankfile = $ARGV[2];

open(RANK,$pageranks) or die;
my %pagerank = ();
while (<RANK>) {
  if (/(\d*)\s.*\[\[(.*)\]\]/) {
    my $page = $2;
    my $number = $1;
    $pagerank{$page} = $number;
  } else {
    die "$_ is weird";
  }
}
close(RANK);

open(BASE,$basepages) or die;
my %bases = ();
while (<BASE>) {
  chomp;
  $bases{$_} = 0;
}
close(BASE);

my %imagerank = ();
my %imagemax = ();

open(OUT,">$imagerankfile") or die;
my $currpage = "";
while(<STDIN>) {
  if (/<title>(.*?)<\/title>/) {
    $currpage = $1;
    unless (exists $pagerank{$currpage}) {
      next;
    }
#print "counting on page $currpage\n";
    my $intext = 0;
    my $readmore = 1;
    my $pagetext = "";
    my %thispageimages = ();
    my $mult = 1;
    if (exists $bases{$currpage}) {
      $mult = $BASEMULT;
    }
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
      }
      $_ = <STDIN>;
    }
    # now $pagetext contains all of this page
    # process pagetext...
#print "pagetext:\n$pagetext\n";
    $pagetext =~ s/\n/ <newline> /g;
    while ($pagetext =~ /.*?&lt;nowiki&gt;.*&lt;\/nowiki&gt;/) {
      $pagetext =~ s/(.*?)&lt;nowiki&gt;.*&lt;\/nowiki&gt;/$1/;
    }
    $pagetext =~ s/(?<!=\[)\[\s*([^\[\]]*?)\s*\](?!\])//g;  # remove all singleton brackets "links" so I can ignore them
    $pagetext =~ s/([^\[])\[([^\[])/$1$2/g;  # remove stranded left brackets
    $pagetext =~ s/([^\]])\]([^\]])/$1$2/g;  # remove stranded right brackets
#print "processed pagetext:\n$pagetext\n";
#print "done processing page\n";
    while ($pagetext =~ /^.*?\[\[\s*([^\[\]]*?)\s*\]\]/s) {
      my $match = $1;
#      print "MATCH $match\n";
      my $link = $match;
      if ($match =~ /^imagen?\s*:\s*(.*)/i) {  # check if it's an image
        my $bracketed = $1;
        my $image = $bracketed;
        my $size = "None";
        if ($bracketed =~ /(.*?)\s*\|(.*)/) {
          $image = $1;
          my $remainder = $2;
          if ($remainder =~ /(\d+)\s*x\s*(\d+)\s*px.*\|/) {
            $size = $1;     # take width if both are specified
          } elsif ($remainder =~ /(\d+)\s*px.*\|/) {
            $size = $1;
          } elsif ($remainder =~ /thumb.*\|/) {
            if ($remainder =~ /upright.*\|/) {
              $size = 140;
            } else {
              $size = 180;    # thumb default to 180 width
            }
          } else {
          }
        }
        $image = capitalize($image);
        $image =~ s/_/ /g;
        if (exists $imagerank{$image}) {
          if (exists $thispageimages{$image}) {
            #print "Don't count $image more than once for $currpage...\n";
          } else {
            #print "Adding to image $image for $currpage...\n";
            $imagerank{$image} += ($mult * $pagerank{$currpage});
            $thispageimages{$image} = 1;
          }
          if ($imagemax{$image} ne "None") {
            if ($size eq "None") {
              $imagemax{$image} = $size;
            } elsif ($imagemax{$image} < $size) {
              $imagemax{$image} = $size;
            }
          }
        } else {
          #print "Creating entry for $image on $currpage...\n";
          $imagerank{$image} = ($mult * $pagerank{$currpage});
          $imagemax{$image} = $size;
          $thispageimages{$image} = 1;
        }
#print "$match [[Imagen:$image]] $imagerank{$image} $pagerank{$currpage}\n";
#      print "remaining pagetext:\n$pagetext\n";
      }
      $pagetext =~ s/^(.*?)\[\[([^\[\]]*?)\s*\]\]/$1/s;  # remove this match from pagetext
    }
  }
}

my @rankedimages = sort {$imagerank{$b} <=> $imagerank{$a}} keys %imagerank;

foreach my $image (@rankedimages) {
#  print "[[Imagen:$image]]\n";
#  print "[[Imagen:$image]]\t$imagerank{$image}\n";
  print OUT "[[Imagen:$image]]\t$imagerank{$image}\t$imagemax{$image}\n";
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
