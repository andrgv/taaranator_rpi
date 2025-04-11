#!/bin/bash
set -e 

echo "Updating package lists and installing required packages..."
sudo apt update && sudo apt install -y python3-pip python3-opencv python3-serial python3-spidev i2c-tools git

echo "Installing Python packages from requirements.txt..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "Enabling SPI and SSH via raspi-config..."
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_ssh 0

echo "Installing systemd taaranator service..."
SERVICE_FILE="taaranator.service"
if [ -f "$SERVICE_FILE" ]; then
    sudo cp "$SERVICE_FILE" /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_FILE"
    echo "Service installed and enabled successfully."
else
    echo "Error: Service file $SERVICE_FILE not found!"
fi