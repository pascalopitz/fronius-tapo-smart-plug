import asyncio
import json
import os
from urllib import request
from PyP100 import PyP100
from dotenv import load_dotenv

load_dotenv()

def get_grid_consumption():
    url = 'http://{ip}/solar_api/v1/GetPowerFlowRealtimeData.fcgi'.format( ip=os.getenv('FRONIUS_IP') )
    f = request.urlopen(url)
    s = json.loads(f.read().decode('utf-8'))
    grid_pull = float(s['Body']['Data']['Site']['P_Grid'])
    pv = float(s['Body']['Data']['Site']['P_PV'])
    load = float(s['Body']['Data']['Site']['P_Load'])
    surplus = pv + load
    print('pv={pv}, load={load}, surplus={surplus}, grid_pull={grid_pull}'.format( pv=pv, load=load, surplus=surplus, grid_pull=grid_pull ))
    return [grid_pull, surplus]


async def main():
    p100 = PyP100.P100(os.getenv('TAPO_SOCKET_IP'), os.getenv('TAPO_EMAIL'), os.getenv('TAPO_PASSWORD')) 
    p100.handshake()
    p100.login()
    info = p100.getDeviceInfo()
    status = info['result']['device_on']
    threshold = float(os.getenv('SURPLUS_THRESHOLD'))
    grid_pull_max = float(os.getenv('GRID_PULL_THRESHOLD'))

    while True:
        [grid_pull, surplus] = get_grid_consumption()
        new_status = (status == True and grid_pull < grid_pull_max) or (status == False and surplus > threshold)

        if status != new_status:
            if new_status == False:
                print('turnOff')
                p100.turnOff()
            else:
                print('turnOn')
                p100.turnOn()

    
        status = new_status
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
task = loop.create_task(main())

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
