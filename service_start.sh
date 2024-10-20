#!/bin/bash

# Copy services from this folder to /etc/systemd/system
echo "Copying services from services folder to /etc/systemd/system"
cp service/* /etc/systemd/system/

# Reload systemd after adding the new services
echo "Reloading systemd daemon after copying services"
systemctl daemon-reload

# Start and enable services from this folder
for service in service/*.service; do
    service_name=$(basename $service)
    echo "Starting and enabling $service_name"
    
    # Start the service
    systemctl start $service_name
    
    # Enable the service to start at boot
    systemctl enable $service_name
done

# Reload systemd to apply changes
echo "Reloading systemd daemon"
systemctl daemon-reload
