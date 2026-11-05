#!/bin/bash
ps aux --sort rss | head -11 | tail -10
