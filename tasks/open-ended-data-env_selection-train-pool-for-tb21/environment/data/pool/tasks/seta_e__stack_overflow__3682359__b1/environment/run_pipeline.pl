#!/usr/bin/env perl
use strict;
use warnings;

print "=== Log Processor Pipeline ===\n";
my @scripts = qw(append_to_log update_runfile archive_entries);
for my $script (@scripts) {
    print "Running $script...\n";
    my $path = "/opt/logprocessor/scripts/${script}.pl";
    do $path;
    if ($@) {
        die "Error in $script: $@\n";
    }
    print "  done.\n";
}
print "=== Pipeline complete ===\n";
