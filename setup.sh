echo "Updating package managers, python and main libraries..."
sudo apt update && sudo apt install -y python3-pip python3-opencv python3-serial  python3-smbus python3-spidev i2c-tools git

echo "Installing python packages..."
pip3 install -r requirements.txt

echo "Enabling I2C and SSH..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_ssh 0

echo "Installing systemd taarantor service..."
sudo cp taaranator.service /etc/systemd/system
sudo systemctl enable taaranator.service