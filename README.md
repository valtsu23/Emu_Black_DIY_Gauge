# EmuB-DIY-Gauge
### Adafruit Feather M4 CAN Express with 2.4" TFT FeatherWing displaying sensor values 

Project goal was to greate small gauge for my Honda S2000 that displays time and sensor values from car ECU. 
Car is equipped with Ecumaster Emu Black ECU that can send data to CAN bus. 

### Hardware: 
- Adafruit Feather M4 CAN Express with ATSAME51 
- Adafruit 2.4" TFT FeatherWing 
- Adafruit DS3231 Precision RTC Breakout 
- 5v regulator circuit
  - 7805 regulator
  - 1uF tantalum capacitor
  - Proto board pcb

### Features: 
- 3 different tabs showing different values and the tab can be changed by touching the screen with finger nail
- Last used tab is saved to SD card and read from there on boot 
- 12V power supply


