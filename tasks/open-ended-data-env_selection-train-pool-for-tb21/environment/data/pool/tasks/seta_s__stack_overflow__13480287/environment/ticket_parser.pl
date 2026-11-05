#!/usr/bin/perl
use strict;
use warnings;

my $input  = '/opt/sensor-pipeline/data/change_log.txt';
my $output = '/opt/sensor-pipeline/output/ticket_ids.txt';

open(my $in, '<', $input) or die "Cannot open $input: $!";
open(my $out, '>', $output) or die "Cannot open $output: $!";

while (my $line = <$in>) {
    chomp $line;
    if ($line =~ /\bCRs?\s*[-:;]?\s*(\d+)/) {
        print $out "$1\n";
    }
}

close $in;
close $out;
