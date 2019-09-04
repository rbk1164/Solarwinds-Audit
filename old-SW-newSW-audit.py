# Author: ROHIT KADAM

import requests
import json

url = 'http://solarwinds-server'
header = {'Content-Type': 'application/json',  'NetOps-API-Key': ''}

output_file = input("Please enter the location of the file where you want to store your output from Solarwinds API:")
output_result = open(output_file,"w")



trt_dumps_file = input("Enter TRT dumps file:")
old_inv = input("Enter old inv file:")
old_inv = open(old_inv, "r").readlines()
old_inv_devices = [row.split(',')[0] for row in old_inv if len(row.split(',')[0].split('-')[0]) is 5]
#print ("OLD_INV:\n", old_inv_devices,"\n\n" )

new_inv = input("Enter new inv file:")
new_inv = open(new_inv, "r").readlines()
new_inv_devices = [row.split(',')[0] for row in new_inv if len(row.split(',')[0].split('-')[0]) is 5]
#print ("NEW_INV:\n", new_inv_devices,"\n\n" )

fp = open(trt_dumps_file)
fp = json.load(fp)

add_devices_to_new = list(set(old_inv_devices)-set(new_inv_devices))
for device in add_devices_to_new:
    if "api" in device or len(device) < 6:
        add_devices_to_new.remove(device)
    else:
        pass

print (add_devices_to_new)
dictionary = {}
start = set()

for each in add_devices_to_new:

    start.add(each[:5])

for each in add_devices_to_new:

    for beg in start:

        if each.startswith(beg):

            if beg in dictionary:

                dictionary[beg].append(each)

            else:

                dictionary[beg] = [each]
        else:
            pass

print(dictionary)



def output_from_sw(output_from_SWv2, payload):
    if 'output' in output_from_SWv2:
        output_result.write("{},{},\n".format(output_from_SWv2["output"][0]["object"], output_from_SWv2["output"][0]["message"]))
    elif 'detail' in output_from_SWv2:
        output_result.write("{},{},\n".format("{}".format(payload[0]["site-code"]),output_from_SWv2["detail"]))
    else:
        output_result.write("{},\n".format(output_from_SWv2))


def pass_to_new_sw(payload):

    add_devices_to_sw = requests.post(url=url, data=json.dumps(payload), headers=header)

    return add_devices_to_sw.json()

def create_payload():
    for key, value in dictionary.items():

        for item in range(len(fp["data"])):

            if str(key).upper() == fp["data"][item]["site_code"]:

                if not fp["data"][item]["functions"] or fp["data"][item]["status"]["name"] == "Closed":
                    pass
                else:

                    payload = [{
        "auto-add-interfaces": "no",
        "city": "{}".format(fp["data"][item]["address"]["city"]),
        "country": "{}".format(fp["data"][item]["address"]["country"]),
        "criticality": "{}".format(fp["data"][item]["store_criticality"]["name"]),
        "hostlist": "{}".format(','.join(dictionary[key])),
        "region": "{}".format(str(fp["data"][item]["region"]["name"]).split("-")[0]),
        "site-code": "{}".format(fp["data"][item]["site_code"]),
        "site-function": "{}".format(fp["data"][item]["functions"][0]["name"].strip())
        }]
                    print (payload)
                    output_from_SWv2 = pass_to_new_sw(payload)
                    output_from_sw(output_from_SWv2, payload)

            else:
                pass

create_payload()
output_result.close()

#C:\Users\rokadam\OneDrive - -\office-work\TRT dumps\trt.json
#C:\Users\rokadam\OneDrive - -\office-work\Inventory Solarwinds\old-SW-inventory.csv
