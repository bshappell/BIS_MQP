
# BIS_MQP
Blisk Inspection MQP

How to run the code project:

// Navigate to the directory
cd Documents/BIS_MQP/

// Set up opencv
source ~/.profile
workon cv

// start pi gpio daemon
sudo pigpiod

// Run the application (must use super user to access gpio)
sudo /home/pi/.virtualenvs/cv/bin/python BisApp.py

