#!/usr/bin/perl
use strict;
use warnings;

my $input  = '/opt/sensor-pipeline/data/tank_sensor.log';
my $output = '/opt/sensor-pipeline/output/tank_levels.txt';

open(my $in, '<', $input) or die "Cannot open $input: $!";
open(my $out, '>', $output) or die "Cannot open $output: $!";

while (my $line = <$in>) {
    chomp $line;
    if ($line =~ m/^(\d{2}:\d{2}),Ull=(\d{3})$/) {
        print $out "$2\n";
    }
}

close $in;
close $out;
