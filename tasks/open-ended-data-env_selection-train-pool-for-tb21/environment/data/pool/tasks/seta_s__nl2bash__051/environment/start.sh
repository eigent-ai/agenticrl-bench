#!/bin/bash
python3 /opt/netio_sim/netio_heavy.py &
python3 /opt/netio_sim/netio_medium.py &
python3 /opt/netio_sim/netio_idle.py &
sleep 4
exec "$@"
