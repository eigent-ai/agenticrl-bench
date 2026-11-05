#!/bin/bash

threshold="10"
node_cpu=$(openstack compute service list --service nova-compute | grep 'enabled' | awk '{print $12}')
max_cpu=$(echo "$node_cpu" | sort -n | tail -n 1)
min_cpu=$(echo "$node_cpu" | sort -n | head -n 1)
if [ $(($max_cpu - $min_cpu)) -gt "$threshold" ]; then
    openstack server migrate --live <instance_id> --host node-compute-1 --block-migration
    echo "Migration triggered"
fi
