#!/bin/bash
# Simulated backup script that generates output and uses CPU
echo "Starting backup at $(date)"
# CPU-intensive operation - calculating prime numbers
count=0
for i in $(seq 1 10000); do
    isprime=1
    for ((j=2; j*j<=i; j++)); do
        if [ $((i % j)) -eq 0 ]; then
            isprime=0
            break
        fi
    done
    if [ $isprime -eq 1 ] && [ $i -gt 1 ]; then
        ((count++))
    fi
done
echo "Backup completed. Found $count primes. Memory usage: $(free -m | awk 'NR==2{print $3}')MB"
echo "WARNING: Backup generated large log output"
