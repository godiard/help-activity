#!/usr/bin/perl

my $blacklist = $ARGV[0];
my $redirects = $ARGV[1];
my $pages = $ARGV[2];

open(BLACK,$blacklist) or die;
my %blacklist = ();
while (<BLACK>) {
  chomp;
  $blacklist{$_} = 0;
}
close(BLACK);

my %redirects = ();
open(REDIR,$redirects) or die;
while (<REDIR>) {
  if (/\[\[(.*)\]\].*\[\[(.*)\]\]/) {
    $redirects{$1} = $2;
  }
}
close(REDIR);

open(PAGE,$pages) or die;
while (<PAGE>) {
  chomp;
  my $inblacklist = 0;
  if (exists $blacklist{$_}) {
    $inblacklist = 1;
  }
  if (exists $redirects{$_}) {
    if (exists $blacklist{$redirects{$_}}) {
      $inblacklist = 1;
    }
  }
  unless ($inblacklist) {
    print "$_\n";
  }
}

