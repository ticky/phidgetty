# Phidgetty

Simple command-line utility to read sensor values from a Phidgets device

## Usage

* `-d <input id>`, `--digital <input id>`: read from a digital input
* `-a <sensor id>`, `--analog <sensor id>`: read from an analog sensor
* `-t`, `--temperature-sensor`: device is a temperature sensor, output in degrees celcius. must be reading an analog sensor
* `-m <multiplier>`, `--precision-light-sensor-multiplier <multiplier>`: 'm' value from the underside of the precision light sensor. must be reading an analog sensor
* `-b <boost>`, `--precision-light-sensor-boost <boost>`: 'b' value from the underside of the precision light sensor. must be reading an analog sensor
