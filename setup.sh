#!/bin/bash
set -e

echo "Updating package lists and installing required packages..."
sudo apt update && sudo apt install -y python3-venv git

echo "Creating and activating Python virtual environment 'env'..."
python3 -m venv env
source env/bin/activate

echo "Installing Python packages from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Enabling SPI and SSH via raspi-config..."
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_ssh 0

echo "Setup complete."