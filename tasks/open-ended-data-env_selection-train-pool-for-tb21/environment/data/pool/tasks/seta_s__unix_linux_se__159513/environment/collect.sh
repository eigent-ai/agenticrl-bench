#!/bin/bash
# Runs the event generator.
# Normal events are written to logs/events.log; debug and error messages go to logs/debug.log.
/opt/pipeline/bin/event_generator &> /opt/pipeline/logs/events.log
