# Author: ROHIT KADAM

import requests
import json
new_inv_file = input("Enter new SW-server inventory:")
new_inv_file = open(new_inv_file).readlines()
count = 0


url = "http://solarwinds-server"
header = {'Content-Type': 'application/json',  'NetOps-API-Key': ''}

def pass_to_API(payload):

    add_devices_to_sw = requests.post(url=url, data=json.dumps(payload), headers=header)

    return add_devices_to_sw.json()


for row in new_inv_file:
    if 'vEdge' in row.split(',')[4]:
        payload = [
            {
             "host": "{}".format(row.split(',')[0]),
             "interfaces": "loopback0"
            }
                   ]
        x = pass_to_API(payload)
        print (x["interfaces"][0]["interface"], x["interfaces"][0]["interfaceStatus"],"\n")

#C:\Users\rokadam\OneDrive - -\office-work\Inventory Solarwinds\new-SW-inventory.csv
