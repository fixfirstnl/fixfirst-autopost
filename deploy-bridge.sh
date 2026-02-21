#!/bin/bash
set -e

# Install systemd service file
sudo cp systemd/fixfirst-autopost.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fixfirst-autopost
sudo systemctl restart fixfirst-autopost
