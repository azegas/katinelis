#!/bin/bash

# Stop and disable services from this folder
for service in service/*.service; do
    service_name=$(basename $service)

    systemctl restart $service_name
    
done
