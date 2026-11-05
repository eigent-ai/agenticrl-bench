#!/usr/bin/perl
use strict;
use warnings;
print "Content-Type: text/plain\n\n";
use LWP::Simple;
my $content = get("http://feeds.bbci.co.uk/news/rss.xml");
print $content // "Failed to fetch feed\n";
