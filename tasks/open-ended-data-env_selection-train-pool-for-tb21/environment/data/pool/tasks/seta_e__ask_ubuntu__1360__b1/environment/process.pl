#!/usr/bin/perl
# Data processing CGI endpoint
use strict;
use warnings;

print "Content-type: text/html\n\n";
print "<html><body>\n";
print "<p>Processing: Starting data processing...</p>\n";

my $data = "sample_data";
print "<p>Processing: Data = $data</p>\n";

print "<p>Processing: Complete</p>\n";
print "</body></html>\n";
exit 0;
