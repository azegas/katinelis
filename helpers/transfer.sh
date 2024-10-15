#!/bin/bash

# Define variables
REMOTE_USER="arvypi"
REMOTE_HOST="192.168.0.82"
REMOTE_PATH="/home/arvypi/GIT/mm2"

# Transfer files using rsync
echo "Transferring files..."
rsync -av --delete \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='.env' \
    --exclude='logs' \
    --exclude='data' \
    --exclude='static/images' \
    ../ "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"

if [ $? -ne 0 ]; then
    echo "Failed to transfer files."
    exit 1
fi

echo "Files transferred successfully."
