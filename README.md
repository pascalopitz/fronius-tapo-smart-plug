# What is this?

Fronius Smart Meter and Tapo P100 = Only running when the sun is shining and we have enough spare juice

Define a surplus threshold and point at your Tapo P100 Socket and Fronius Smart Meter.
The socket will then be switched on and off depending on whether the available solar surplus threshold is met.
Useful for running a device like a heater.
 
## Prerequisites

You will need a Fronius Smart Meter installed and exosed via an IP address.

You will also need a [Tapo P100 smart plug](https://www.tp-link.com/au/home-networking/smart-plug/tapo-p100/) and have it registered in the Tapo app and visible via a known IP address.

# Get started

1. Create a `.env` file from the `.env.example` and provide the blank values matching your home setup.

2. Install Dependencies

```bash
sudo apt install python3-pip
pip3 install PyP100 python-dotenv asyncio
```
3. Run script

```bash
python3 index.py
```

## Fronius Smart Meter data

We're using the `GetPowerFlowRealtimeData.cgi` call.
See the [Fronius API Docs](https://www.fronius.com/~/downloads/Solar%20Energy/Operating%20Instructions/42,0410,2012.pdf).


## Library for Tapo P100 control

Utilising [https://github.com/fishbigger/TapoP100](https://github.com/fishbigger/TapoP100)

