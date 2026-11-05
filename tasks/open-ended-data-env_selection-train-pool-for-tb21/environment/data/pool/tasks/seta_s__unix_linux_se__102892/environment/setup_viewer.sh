#!/bin/bash
# Configure the less pager with syntax highlighting
export LESSOPEN="| /usr/bin/src-hilite-lesspipe.sh %s"
export LESS="-R"
