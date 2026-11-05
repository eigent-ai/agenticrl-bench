#!/bin/bash
set -e

cd /opt/binpack

mkdir -p output

bin/writer data/input.csv output/packed.bin
bin/reader output/packed.bin output/unpacked.csv

diff -q unpacked.csv input.csv
