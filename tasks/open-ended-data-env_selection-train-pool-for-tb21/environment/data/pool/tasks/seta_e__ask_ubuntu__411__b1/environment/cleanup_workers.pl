#!/usr/bin/perl
# Cleanup script for stale worker processes

use strict;
use warnings;

# Load configuration (parse simple KEY=VALUE config file)
my %config;
open(my $cfg, '<', '/opt/config/config.conf') or die "Cannot open config: $!";
while (<$cfg>) {
    chomp;
    next if /^\s*#/ || /^\s*$/;
    if (/^(\w+)=(.*)$/) {
        my ($key, $val) = ($1, $2);
        $val =~ s/^"(.*)"$/$1/;  # strip quotes
        $config{$key} = $val;
    }
}
close($cfg);

print "Starting cleanup process...\n";

# Find and collect target process PIDs
my @output = `ps aux`;
my @pids_to_kill;
for my $line (@output) {
    if ($line =~ /(server|worker)/ && $line !~ /grep/) {
        my @fields = split(/\s+/, $line);
        push @pids_to_kill, $fields[1];
    }
}

# Terminate collected processes
for my $pid (@pids_to_kill) {
    print "Killing process $pid\n";
    kill 9, $pid;
}

print "Cleanup complete\n";
