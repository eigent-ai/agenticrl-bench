#!/usr/bin/perl
use strict;
use warnings;

my $input  = '/opt/sensor-pipeline/data/config_values.txt';
my $output = '/opt/sensor-pipeline/output/config_entries.txt';

open(my $in, '<', $input) or die "Cannot open $input: $!";
open(my $out, '>', $output) or die "Cannot open $output: $!";

while (my $line = <$in>) {
    chomp $line;
    if ($line =~ /(telco_imac_)city|(telco_hier_)city/) {
        my $prefix = $1;
        $prefix =~ s/_$//;
        my ($value) = $line =~ /=(.+)/;
        print $out "$prefix=$value\n";
    }
}

close $in;
close $out;
