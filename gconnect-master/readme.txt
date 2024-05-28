# About
This small program is used to connect the FlightGear flight simulator to the LittleNavMap.
To make this application run, please install the FlightGear Addon from the following link:
  - https://github.com/slawekmikula/flightgear-addon-littlenavmap

I have implemented this program since I did not want to compile (in MacOS) the official
application "littlefgconnect"; also, the official application does not connect directly
between FlightGear and LittleNavMap, but requires LittleNavConnect inbetween.

Except for the add-on, this program does not require anything else to be running on the
machine. To use it, just provide the IP address/server name and port number of the
machine running FlighGear + Addon, and also provide the IP address/server name and port
number of the machine running LittleNavMap. Click start (on both Start buttons for
FlightGear, and LittleNavMap) and enjoy!

Note 1:
  I have only tested this software in MacOS; however it should also run in Windows and
  also in Linux

Note 2:
  I am currently running the program directly from Python, on MacOS; however I might
  provide some packaged versions for MacOS, Windows, and Linux in the future

######################
# Necessary Packages #
######################
The list below shows the python packages that are required to run this program. To install
them, simply run the shown commands

pip3 install xmltodict
pip3 install wxpython
