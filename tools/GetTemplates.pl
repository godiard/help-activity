#!/usr/bin/perl

use warnings;
use strict;

my $allpagelist = $ARGV[0];
my $redirects = $ARGV[1];
my $pagelist = $ARGV[2];
my $out = $ARGV[3];

open(OUT,">$out") or die;

my %allpages = ();
open(PAGE,$allpagelist) or die;
while (<PAGE>) {
  chomp;
  $allpages{$_} = 0;
}
close(PAGE);

my %redirects = ();
open(REDIR,$redirects) or die;
while(<REDIR>) {
  if (/\[\[(.*)\]\].*\[\[(.*)\]\]/) {
    $redirects{$1} = $2;
  }
}

my %pages = ();
open(PAGE,$pagelist) or die;
while(<PAGE>) {
  chomp;
  $pages{$_} = 0;
}
close(PAGE);

my %templates = ();

my $currpage = "";
while (<STDIN>) {
  if (/<title>(.*?)<\/title>/) {
    $currpage = $1;
    unless (exists $pages{$currpage}) {
      next;
    }
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
        if (length($pagetext) > 300000) {
          last;
        }
      }
      $_ = <STDIN>;
    }
    $pagetext =~ s/\n/ <newline> /g;
    $pagetext =~ s/(?<!=\{)\{({^\{\}}*?)\s*\}(?!\})//g;  # remove all singleton brackets "links" so I can ignore them
    $pagetext =~ s/({^\{})\{({^\{})/$1$2/g;  # remove stranded left brackets
    $pagetext =~ s/({^\}})\}({^\}})/$1$2/g;  # remove stranded right brackets
    #print "\"$currpage\"";
    while ($pagetext =~ /.*?\{\{\s*([^\{\}]*?)\s*\}\}/s) {
      my $bracketed = $1;
      my $template = $bracketed;
      $pagetext =~ s/(.*?)\{\{\s*([^\{\}]*?)\s*\}\}//s;
      if ($bracketed =~ /^(.*?)\s*[<\|]/) {
        $template = $1;
      }
      if ($template =~ /DEFAULTSORT/) {
        next;
      }
      if ($template =~ /Plantilla:\s*(.*)/i) {
        $template = $1;
      }
      $template = capitalize($template);
      $template =~ s/_/ /g;
      $template = "Plantilla:" . $template;
      unless (exists $allpages{$template}) {
        next;
      }
      if (exists $templates{$template}) {
        #$templates{$template}++;
      } else {
        $templates{$template} = 1;
        print OUT "$template\n";
      }
      if (exists $redirects{$template}) {
        if (exists $templates{$redirects{$template}}) {
        } else {
          $templates{$redirects{$template}} = 1;
          print OUT "$redirects{$template}\n";
        }
      }
    }
  }

}

my @sorted = sort {$templates{$b} <=> $templates{$a}} keys %templates;

#foreach my $temp (@sorted) {
#  print OUT "[[$temp]]\t$templates{$temp}\n";
#}


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

