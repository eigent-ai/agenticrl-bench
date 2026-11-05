#!/bin/bash
# Startup script for the Status API backend

PIDFILE="/var/run/statusapi.pid"
LOGFILE="/var/log/statusapi.log"

case "$1" in
    start)
        if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            echo "statusapi is already running (PID $(cat $PIDFILE))"
            exit 0
        fi
        echo "Starting Status API..."
        su statusapi -c "python3 /opt/statusapi/main.py" >> "$LOGFILE" 2>&1 &
        echo $! > "$PIDFILE"
        echo "Started with PID $!"
        ;;
    stop)
        if [ -f "$PIDFILE" ]; then
            kill $(cat "$PIDFILE") 2>/dev/null
            rm -f "$PIDFILE"
            echo "Stopped."
        else
            echo "Not running."
        fi
        ;;
    status)
        if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            echo "running (PID $(cat $PIDFILE))"
        else
            echo "stopped"
        fi
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
