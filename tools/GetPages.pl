#!/usr/bin/perl

use strict;
use warnings;

my $pages = $ARGV[0];
my $redirects = $ARGV[1];

open(PAGES,">$pages") or die;
open(REDIR,">$redirects") or die;

my %pagerank = ();
my %redirects = ();
my $currpage = "";
while (<STDIN>) {
  if (/<title>(.*?)<\/title>/) {
    my $pagetitle = $1;
    $pagerank{$1} = 0;
    $currpage = $1;
    print PAGES "$currpage\n";
  }
  if (/#REDIRECT:?\s*\[\[\s*(.*?)\s*\]\]/i) {
    my $bracketed = $1;
    if ($bracketed =~ /:Categ/i) {
      $bracketed =~ s/:(Categ)/$1/i;
    }
    my $redirectpage = $bracketed;
    if ($bracketed =~ /(.*?)\s*[#\|]/) {
      $redirectpage = $1;
    }
    $redirectpage = capitalize($redirectpage);
    $redirectpage =~ s/_/ /g;
    unless (exists $redirects{$currpage}) {
      $redirects{$currpage} = $redirectpage;
    }
    print REDIR "[[$currpage]]\t[[$redirectpage]]\n";
  } 
}

sub capitalize {
  my $word = shift;
  #print "$word to ";
  my $firstletter = substr($word,0,1);
  if ($firstletter =~ /[a-z]/) {
    my $newletter = uc($firstletter);
    substr($word,0,1) = $newletter;
  }
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
