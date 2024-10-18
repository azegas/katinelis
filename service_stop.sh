# Stop and disable services from this folder
for service in service/*.service; do
    service_name=$(basename $service)
    echo "Stopping and disabling $service_name"
    
    # Stop the service if running
    systemctl stop $service_name
    
    # Disable the service to prevent it from starting at boot
    systemctl disable $service_name
    
    # Remove the service file from /etc/systemd/system
    echo "Removing $service_name from /etc/systemd/system"
    rm /etc/systemd/system/$service_name
done

# Reload systemd to apply changes
echo "Reloading systemd daemon"
systemctl daemon-reload
