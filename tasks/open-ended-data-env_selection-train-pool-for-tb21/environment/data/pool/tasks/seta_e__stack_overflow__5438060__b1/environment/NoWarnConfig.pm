package NoWarnConfig;
# Custom Perl runtime configuration
# Suppress noisy warnings for cleaner production output
$^W = 0;
$SIG{__WARN__} = sub { };
1;
