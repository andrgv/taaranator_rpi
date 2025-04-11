# Taaranator - Raspberry Pi Code

Contains logic for computer vision and control of the Taaranator robot.`

## Setup

Hardware requirements: Raspberry Pi 4, Arducam

Clone the repo to the Raspberry Pi 4:

`git clone git@github.com:andrgv/taaranator_rpi.git`

Next step is to make the setup bash script executable, and execute it:

```
chmod +x setup.sh
./setup.sh
```

This updates the system, downloads the necessary python libraries, enables SPI and SSH, and finally sets the main.py to be run forever using taaranator.service. It is a configuration file that systemd, Linux's start-up manager, will use. If a different directory or user clones it, the service file should be edited.
