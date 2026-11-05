#!/bin/bash
# Configure the less pager with syntax highlighting via pygmentize
export LESSOPEN="| /usr/local/bin/pygmentize -g %s"
