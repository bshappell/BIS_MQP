
# BIS_MQP
Blisk Inspection MQP

How to run the code project:

// Navigate to the directory
cd Documents/BIS_MQP/entityClasses

// Set up opencv
source ~/.profile
workon cv

// Configure the gpio 
sudo pigpiod

// Run the application (must use super user to access gpio)
sudo /home/pi/.virtualenvs/cv/bin/python BisApp.py

The application can instead be run by double clicking the Blisk Inspection System Icon on the Desktop of the Raspberry Pi.



Below are the instructions to set up the wiring for the system:
In order to properly wire the system together, there are a few important steps to follow:

1.) First, set up the Raspberry Pi using a mouse, keyboard, and HDMI monitor. Connect the ribbon cable from the Raspberry Pi to the ribbon cable connector on the auxiliary electrical board. Close the Raspberry Pi enclosure to protect the circuitry.

2.) Next, connect the 12V supply to the auxiliary electrical board using the barrel connector, but do not connect it to mains power.
Connect the cooling fan to the fan connection pins on the auxiliary electrical board.

3.) Close the enclosure for the auxiliary electrical board, ensuring that all connectors are outside the box and accessible. 

4.) Connect the stepper motor to the 4-pin connector with red, black, yellow, and white wires.

5.) Connect the load cell to the 4-pin connector with red, black, green, and white wires.

6.) Connect the servo to the 3-pin connector with red, black, and yellow wires.

7.) Connect the LED and contact sensor (one connector) to the auxiliary electrical board connector with red, black, and white wires.

8.) Connect the USB camera from the EOAT to the Raspberry Pi.

9.) Once all connections are made, supply electrical power to the external 12V power supply.


Below are the instructions to use the application:

This application can be used to inspect the following GE Bladed Disks (Blisks): 2468M19P01, 2468M17P02, and 2468M18G02. Ensure that the IRC5 Controller for the ABB Robotic Arm IRB1600T is powered on. The Raspberry Pi must be on and the wiring must be set up according to the wiring diagram. The End of Arm Tooling (EOAT) must be mounted to the ABB Robot with the correct ball gauge attached. When viewed from the camera side (the camera is on top, looking down onto the EOAT) the small ball gauge is the left arm. Once everything is connected, start up the blisk inspection application.  Click the button to home the arm and select a blisk to inspect. Place the blisk on the turntable, but do not tighten it down. Select the button in the application to position the tooling just outside of the blisk. Ensure that the arm is lined up between the blades, with the blade to its right being the first to be inspected. Ensure that the grounding clip is on the blisk before turning the turntable with the application, and remove it afterwards. After this the inspection process will run, and when it is complete the application will identify where the results CSV file can be found. 




