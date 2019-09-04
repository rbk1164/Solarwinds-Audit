# Author: ROHIT KADAM

import requests
import json


url = 'http://solarwinds-server'
header = {'Content-Type': 'application/json',  'NetOps-API-Key': ''}

trt_dumps_file = input("Enter TRT dumps file:(.json)")
fp = open(trt_dumps_file)
fp = json.load(fp)


output_file = input("Please enter the location of the file where you want to store your output from Solarwinds API:(.csv)")
output_result = open(output_file,"w")


NB_weekly_discovery = input("Please enter Netbrain weekly dioscvery file:(.csv)")

NB_weekly_discovery = open(NB_weekly_discovery).readlines()
NB_weekly_discovered_devices = []
for row in NB_weekly_discovery:
    if '-api-' in row.split(',')[0] or '-' not in row.split(',')[0]:
        pass
    else:
        NB_weekly_discovered_devices.append((row.split(',')[0]))

NB_weekly_discovered_devices = list(set(NB_weekly_discovered_devices))

site_and_devices = {}
start = set()

for each in NB_weekly_discovered_devices:

    start.add(each[:5])

for each in NB_weekly_discovered_devices:

    for beg in start:

        if each.startswith(beg):

            if beg in site_and_devices:

                site_and_devices[beg].append(each)

            else:

                site_and_devices[beg] = [each]
        else:
            pass

print(site_and_devices)



def output_from_sw(output_from_SWv2, payload):
    for key, value in output_from_SWv2.items():
        if key=="output":
            for item in output_from_SWv2["output"]:
                output_result.write("{},{},\n".format(item["object"],item["message"]))

    if 'detail' in output_from_SWv2:
        output_result.write("{},{},\n".format("{}".format(payload[0]["site-code"]),output_from_SWv2["detail"]))
    else:
        pass

def pass_to_new_sw(payload):

    add_devices_to_sw = requests.post(url=url, data=json.dumps(payload), headers=header)

    return add_devices_to_sw.json()

def create_payload():
    for key, value in site_and_devices.items():

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
        "hostlist": "{}".format(','.join(site_and_devices[key])),
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





#output: nb-weekly-discovery-to-sw.csv
#TRT: C:\Users\rokadam\OneDrive - -\office-work\TRT dumps\trt.json
#input: C:\Users\rokadam\OneDrive - -\office-work\Netbrain-weeklydiscover\netbrain-discovery-diff.csv
