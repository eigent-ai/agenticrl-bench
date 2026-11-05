#!/bin/bash
mkdir -p /data/db /var/log/mongodb
mongod --fork --logpath /var/log/mongodb/mongod.log --dbpath /data/db
sleep 2
exec "$@"
