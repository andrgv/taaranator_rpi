#!/bin/bash
set -e 

echo "Updating package lists and installing required packages..."
sudo apt update && sudo apt install -y git

echo "Starting virtual environment"
source onnx-env/bin/activate

echo "Installing Python packages from requirements.txt..."
pip install requirements.txt

echo "Enabling SPI and SSH via raspi-config..."
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_ssh 0