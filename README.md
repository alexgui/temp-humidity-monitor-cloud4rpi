# Temperature/Humidity Monitor for Raspberry Pi Using Cloud4Rpi
This project contains code for a temperature/humidity monitor for the Raspberry Pi with visualization via a Cloud4Rpi dashboard. It is heavily influenced by the project documented [here](https://cloud4rpi.io/raspberry-pi-projects/humidity-in-the-cloud), but with modifications for my use case.

# Use Case/Motivation
The primary motivation for this project is to remotely monitor the temperature in my beer cellar, which consists of a chest freezer controlled by a digital temperature controller. Chest freezers are relatively affordable bulk storage, but need some add-ons to function properly (i.e. not freeze your beer). For the digital temperature controller, I decided a COTS device widely used in the homebrewing world would be the easiest and most cost-effective solution: [Inkbird ITC-308](https://www.amazon.com/Inkbird-Itc-308-Temperature-Controller-Thermostat). This two-stage controller switches on/off the freezer for the cooling function, and a resistive heating pad for the heating function.

However, one major drawback of using the Inkbird ITC-308 (or any similar device, really), is that the temperature probes are prone to single point failure. In this case, if it fails erroneously high and triggers the freezer to turn on, all my beer could potentially freeze! If it fails erroneously low, the heating pad will turn on and my beer might get a little warm but the heating pad itself can't get much warmer than 80 degF.

I had a Raspberry Pi and some temperature sensors leftover from another project, so I figured I could easily build a device to monitor the temperature (and humidity!) inside the chamber. By connecting it to a free dashboard service, I could set the dashboard up for easy visualization as well as over/under temperature alerts.

I ended up using a BME280 to measure the temperature and humidity inside the cellar, and a BMP280 to monitor the ambient temperature outside. [Adafruit](https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout) has good documentation on how to wire up the devices. All parameters were calibrated against the ITC-308 reading, as well as an independent temperature/humidity sensor device.

The Cloud4Rpi dashboard is set up to monitor cellar temperature, cellar humidity, and ambient temperature, as well as issue email alerts for over/under temperature instances:

<img width="887" alt="Screen Shot 2021-05-06 at 1 07 03 PM" src="https://user-images.githubusercontent.com/10524839/117359323-1364b480-ae6c-11eb-8b5e-255101e65b4c.png">
<img width="1153" alt="Screen Shot 2021-05-06 at 1 07 17 PM" src="https://user-images.githubusercontent.com/10524839/117359331-13fd4b00-ae6c-11eb-81cb-caa3a3f591b6.png">
<img width="1154" alt="Screen Shot 2021-05-06 at 1 07 29 PM" src="https://user-images.githubusercontent.com/10524839/117359336-15c70e80-ae6c-11eb-84f5-8e4d4c600520.png">

At the time of writing, I have the ITC-308 set to target 50 degF, and the cooling/heating functions to turn on at +/- 3 degF from the target (i.e. the operating window is 47-53 degF. This seems to be a good balance between cooling/heating cycles.

If you want to see some photos of the cellar in operation, check out my [Instagram highlights](https://www.instagram.com/stories/highlights/17899675735770426/) (best viewed in the app).

# Getting Started
1. Download the repo: ```git pull https://github.com/alexgui/temp-humidity-monitor-cloud4rpi.git```
2. Make an account at [Cloud4Rpi](cloud4rpi.io). At the time of writing, a free account gets 5,000 packets (data transmission that can include multiple parameters) a month.
3. Create a new device at Cloud4RPi
4. Populate the ```DEVICE_TOKEN``` parameter in ```temp_hum_monitor_cloud4rpi.py```
5. Execute the script:
    ```python3 temp_hum_monitor_cloud4rpi.py```
