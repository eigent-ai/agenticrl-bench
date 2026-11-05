#!/bin/bash
input=$1
grep -v '^#' "$input" > "$input"
