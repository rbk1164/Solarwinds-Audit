# Author: ROHIT KADAM

import requests
import json
import logging

logging.basicConfig(
    filename='debug.log',
    level=logging.INFO,
)

sites = "a, b, c"
device_types = ['1', '2', '3', '4']
dictionary = {}
print (sites.split(','))
for each in [x.strip() for x in sites.split(',')]:
    for device_type in device_types:
        if each in dictionary:
            dictionary[each].append(each+device_type)
        else:
            dictionary[each] = [each+device_type]

print(dictionary)

#*********************************************** Solarwinds Block Start ******************************************************************
def if_solarwinds():
    url = 'http://solarwinds-server'
    header = {'Content-Type': 'application/json',  'NetOps-API-Key': ''}
    output_file = input("Please enter the location of the file where you want to store your output from Solarwinds API:")
    output_result = open(output_file,"w")
    trt_dumps_file = input("Enter TRT dumps file:")
    fp = open(trt_dumps_file)
    fp = json.load(fp)
    create_payload(fp, output_result, url, header)
    output_result.close()

def pass_to_new_sw(payload, url, header):
    add_devices_to_sw = requests.post(url=url, data=json.dumps(payload), headers=header)
    return add_devices_to_sw.json()

def output_from_sw(output_from_SWv2, payload, output_result):
    for key, value in output_from_SWv2.items():
        if key=="output":
            for item in output_from_SWv2["output"]:
                output_result.write("{},{},\n".format(item["object"],item["message"]))

    if 'detail' in output_from_SWv2:
        output_result.write("{},{},\n".format("{}".format(payload[0]["site-code"]),output_from_SWv2["detail"]))
    else:
        pass

def create_payload(fp, output_result, url, header):
    fp = fp['data']
    for item in fp:
        #print(item)
        if item["site_code"]:
            if item["site_code"].lower() in dictionary:

                if not item["functions"] or item["status"]["name"] == "Closed":
                    pass
                else:

                    payload = [{
        "auto-add-interfaces": "no",
        "city": "{}".format(item["address"]["city"]),
        "country": "{}".format(item["address"]["country"]),
        "criticality": "{}".format(item["store_criticality"]["name"]),
        "hostlist": "{}".format(','.join(dictionary[item["site_code"].lower()])),
        "region": "{}".format(str(item["region"]["name"]).split("-")[0]),
        "site-code": "{}".format(item["site_code"]),
        "site-function": "{}".format(item["functions"][0]["name"].strip())
        }]
                    print (item["site_code"].lower(), payload)
                    output_from_SWv2 = pass_to_new_sw(payload, url, header)
                    output_from_sw(output_from_SWv2, payload, output_result)

            else:
                logging.info(f'Site code {item["site_code"]} not in dict')
                pass
        else:
            logging.info(f'Failed on {item["id"]}')
#*********************************************** Solarwinds Block End ******************************************************************


#*********************************************** Netbrain Block Start ******************************************************************
def if_netbrain():
    url = 'http://netbrains-server'
    header = {'Content-Type': 'application/json',  'NetOps-API-Key': ''}
    output_file = input("Please enter the location of the file where you want to store your output from Netbrain API:")
    output_result = open(output_file,"w")
    pass_to_NB(url, header, output_result)

def pass_to_NB(url, header, output_result):
    all_devices_list = []
    for key, value in dictionary.items():
        all_devices_list.append(','.join(value))
    payload = [
      {
        "hostlist": "{}".format(','.join(all_devices_list))
      }
    ]
    print (payload)
    add_devices_to_nb = requests.post(url=url, data=json.dumps(payload), headers=header)
    print(add_devices_to_nb.json())
    output_result.write(str(add_devices_to_nb.json()))
    output_result.close()
#*********************************************** Netbrain Block End******************************************************************


def choice_is_yours():
    Choice = input("Please enter where do you want to POST info to:\nPress 1 for Solarwinds, Press 2 for Netbrain:")
    if Choice == '1':
        pass
        #if_solarwinds()

    elif Choice == '2':
        if_netbrain()

    else:
        print("Pelase enter valid input")
        choice_is_yours()


choice_is_yours()

#SW: sw_test_output.csv
#NB: nb_test_output.txt
#C:\Users\rokadam\OneDrive - -\office-work\TRT dumps\trt.json
