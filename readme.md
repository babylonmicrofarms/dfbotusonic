# DFRobot Ultrasonic Sensor A02YYUW python driver

This repo is intended to make a configurable driver for the A02YYUW DFRobot ultrasonic driver.

## Table of Contents

[Hardware Integration](#hardwareintegration)  
[Features](#features)  
[Quickstart](#quickstart)  
[Credits](#credits)  

## Hardware Integration

The sensor uses the UART protocol to communicate. To integrate with a compatibile computer or microcontroller, connect the appropriate wires from the sensor to the UART bus pins of the MCU or use a UART to USB cable and connet to an available USB port of the compatible device. 

See the [Product Wiki](https://wiki.dfrobot.com/_A02YYUW_Waterproof_Ultrasonic_Sensor_SKU_SEN0311) for more info.

## Features

[x] Specify which serial COM port to communicate over.  
[x] Set the range of acceptable ranges in the setup. Default is 0-4500 mm.  
[x] Get the latest distance reading.  
[x] Check the status of the latest reading.  

## Quickstart

git clone or pip install this repo

To run the demo first make sure that your user has proper permissions to access the device com port. Then:

```bash

python3 demo.py

```

## Credits

·author [Arya xue.peng@dfrobot.com]
