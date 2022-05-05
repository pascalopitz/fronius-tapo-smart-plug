# What is this?

Fronius and Tapo = Only running when the sun is shining

Define a surplus threshold and point at your Tapo Socket.
The socket will then be switched on and off depending on the available solar surplus.
Useful for running a device like a heater.
 

## Prerequisites

```bash
sudo apt install python3-pip
```

## Tapo P100 control

Utilising [https://github.com/fishbigger/TapoP100](https://github.com/fishbigger/TapoP100)

```bash
pip3 install PyP100 python-dotenv asyncio
```

# Run

```bash
python3 index.py
```