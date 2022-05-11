import asyncio
import json
import os
import signal
import sys
from urllib import request

from dotenv import load_dotenv
from PyP100 import PyP100

load_dotenv()

timeout = 10

def get_grid_consumption():
    url = 'http://{ip}/solar_api/v1/GetPowerFlowRealtimeData.fcgi'.format( ip=os.getenv('FRONIUS_IP') )
    f = request.urlopen(url)
    s = json.loads(f.read().decode('utf-8'))
    grid_pull = float(s['Body']['Data']['Site']['P_Grid'] or 0)
    pv = float(s['Body']['Data']['Site']['P_PV'] or 0)
    load = float(s['Body']['Data']['Site']['P_Load'] or 0)
    surplus = pv + load
    print('pv={pv}, load={load}, surplus={surplus}, grid_pull={grid_pull}'.format( pv=pv, load=load, surplus=surplus, grid_pull=grid_pull ))
    return [grid_pull, surplus]

async def interation(p100, on_threshold, off_threshold, status):
    while True:
        try:
            [grid_pull, surplus] = get_grid_consumption()
            new_status = (status == True and grid_pull < off_threshold) or (status == False and surplus > on_threshold)

            if status != new_status:
                if new_status == False:
                    print('turnOff')
                    p100.turnOff()
                else:
                    print('turnOn')
                    p100.turnOn()

            status = new_status
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")

        await asyncio.sleep(timeout)

def main():
    loop = asyncio.new_event_loop()

    p100 = PyP100.P100(os.getenv('TAPO_SOCKET_IP'), os.getenv('TAPO_EMAIL'), os.getenv('TAPO_PASSWORD'))
    p100.handshake()
    p100.login()
    info = p100.getDeviceInfo()
    status = info['result']['device_on']
    print('Device on={status}'.format(status=status))
    on_threshold = float(os.getenv('DEVICE_WATTAGE')) - float(os.getenv('GRID_PULL_WATTAGE_MAX'))
    off_threshold = float(os.getenv('GRID_PULL_WATTAGE_MAX'))

    async def exit():
        print('turnOff')
        p100.turnOff()
        print("Stop")
        loop.stop()

    def ask_exit():
        task.cancel()
        asyncio.ensure_future(exit())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, ask_exit)

    task = loop.create_task(interation(p100=p100, on_threshold=on_threshold, off_threshold=off_threshold, status=status))

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    main()