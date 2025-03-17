# Emu_Black_DIY_Gauge
### Adafruit Feather M4 CAN Express with 2.4" TFT FeatherWing displaying sensor values 

Project goal was to create a small gauge for my Honda S2000 that displays time and sensor values from car ECU. 
Car is equipped with Ecumaster Emu Black ECU that can send data to CAN bus. Power supply for the device is 12v. 

### Hardware: 
- Adafruit Feather M4 CAN Express with ATSAME51 
- Adafruit 2.4" TFT FeatherWing 
- Adafruit DS3231 Precision RTC Breakout 
- JST-SM 4pin connector
- 5v regulator circuit
  - 7805 regulator
  - 1uF 35v tantalum capacitor
  - Proto board pcb
 
### Case
- Original desing (feather-tft-case): https://www.thingiverse.com/thing:2209964/files
- I removed the hole for the switch and added hole for the connector
- 3d printed from PETG
- 4 x M2.5 Machine Screws

### Cost
- Parts in total about 80€ 
- Case was 20€ printed by a hobbyist

### Display features: 
- 3 different tabs showing different values and the tab can be changed by touching the screen
- Last used tab is saved to SD card and read from there on boot 
- Video of the working display: https://youtu.be/Mr_nFbw4OqU

### Wiring notices
- DS3231 VIN to Feather 3V pin
- Capacitor on input side of the regulator 
- Regulator output connected to USB-pin on Feather (not the recommended way, because it might damage the computer plugged to usb-port)
More info: https://learn.adafruit.com/adafruit-feather-m0-basic-proto/power-management

### Understanding how it works
- The code.py file contains the main code. I have used many examples to build the code.
- Data showed on the diplay is split in several goups. There is one main group and 5 lower groups. Data of the 4 groups is changed during the tab change. 
Check links 1 and 2 about controlling the display. 
- Link 3 helps you undestand the Can-Bus communication. 
- I'm using Struct library to unpack the Can-Bus messages (links 4 and 5)

### Useful links
1. https://learn.adafruit.com/adafruit-2-4-tft-touch-screen-featherwing/2-4-tft-featherwing
2. https://learn.adafruit.com/circuitpython-display-support-using-displayio/library-overview
3. https://learn.adafruit.com/using-canio-circuitpython
4. https://docs.python.org/3/library/struct.html
5. https://en.wikipedia.org/wiki/C_data_types

![image1](https://github.com/valtsu23/Pictures/blob/main/Emu_Black_DIY_Gauge/IMG_20210524_143746.jpg)

![image2](https://github.com/valtsu23/Pictures/blob/main/Emu_Black_DIY_Gauge/IMG_20210524_143809.jpg)

![image3](https://github.com/valtsu23/Pictures/blob/main/Emu_Black_DIY_Gauge/IMG_20210524_143826.jpg)

![image4](https://github.com/valtsu23/Pictures/blob/main/Emu_Black_DIY_Gauge/IMG_20210331_225259.jpg)
