#!/usr/bin/perl
use strict;
use warnings;

my $input  = '/opt/sensor-pipeline/data/sip_log.txt';
my $output = '/opt/sensor-pipeline/output/network_endpoints.txt';

open(my $in, '<', $input) or die "Cannot open $input: $!";
open(my $out, '>', $output) or die "Cannot open $output: $!";

while (my $line = <$in>) {
    chomp $line;
    next unless $line =~ /sip:/;
    my $addr = $line;
    $addr =~ s/.*sip://;
    $addr =~ s/\s.*//;
    $addr =~ s/(sip:)(;.*)//;
    print $out "$addr\n";
}

close $in;
close $out;
