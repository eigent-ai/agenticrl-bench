#!/bin/sh
# Mock rc-update for container environment
case "$1" in
    del|delete)
        service="$2"
        runlevel="${3:-default}"
        link="/etc/runlevels/$runlevel/$service"
        if [ -L "$link" ] || [ -e "$link" ]; then
            rm -f "$link"
            echo " * service $service removed from runlevel $runlevel"
        else
            echo " * service $service is not in runlevel $runlevel"
        fi
        ;;
    add)
        service="$2"
        runlevel="${3:-default}"
        mkdir -p "/etc/runlevels/$runlevel"
        ln -sf "/etc/init.d/$service" "/etc/runlevels/$runlevel/$service"
        echo " * service $service added to runlevel $runlevel"
        ;;
    show)
        echo "Runlevel: default"
        for f in /etc/runlevels/default/*; do
            [ -e "$f" ] && echo "  $(basename "$f")"
        done
        ;;
    *)
        echo "Usage: rc-update {add|del|show} [service] [runlevel]"
        ;;
esac
