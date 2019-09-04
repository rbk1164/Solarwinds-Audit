# Author: ROHIT KADAM

import requests
import json
fp = open("sw_output.csv").readlines()
print (fp)

fp1 = open("C:\\Users\\rokadam\\OneDrive - -\\office-work\\Inventory Solarwinds\\old-SW-inventory.csv").readlines()
print (fp1)


DNS_not_set = []
for row in fp:
    if 'DNS' in row:
        DNS_not_set.append(row.split(',')[0])
    else:
        pass
print (DNS_not_set)
print (len(DNS_not_set))

dictionary = {}
start = set()
for each in DNS_not_set:

    start.add(each[:5])


def ip_add(each):
    for row in fp1:
        print (row)
        if each in row and "Inc" in row:
            return row.split(",")[3]
        elif each in row:
            return row.split(",")[2]
        else:
            pass


for each in DNS_not_set:
    print(each)
    for beg in start:

        if each.startswith(beg):

            if beg in dictionary:

                dictionary[beg].append("{}".format(ip_add(each)))

            else:

                dictionary[beg] = [ip_add(each)]
        else:
            pass

print (dictionary)



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



fp2 = open("C:\\Users\\rokadam\\OneDrive - -\\office-work\\TRT dumps\\trt.json")
fp2 = json.load(fp2)
def create_payload():
    for key, value in dictionary.items():

        for item in range(len(fp2["data"])):

            if str(key).upper() == fp2["data"][item]["site_code"]:

                if not fp2["data"][item]["functions"] or fp2["data"][item]["status"]["name"] == "Closed":
                    pass
                else:

                    payload = [{
        "auto-add-interfaces": "no",
        "city": "{}".format(fp2["data"][item]["address"]["city"]),
        "country": "{}".format(fp2["data"][item]["address"]["country"]),
        "criticality": "{}".format(fp2["data"][item]["store_criticality"]["name"]),
        "hostlist": "{}".format(','.join(dictionary[key])),
        "region": "{}".format(str(fp2["data"][item]["region"]["name"]).split("-")[0]),
        "site-code": "{}".format(fp2["data"][item]["site_code"]),
        "site-function": "{}".format(fp2["data"][item]["functions"][0]["name"].strip())
        }]
                    print (payload)
                    #output_from_SWv2 = pass_to_new_sw(payload)
                    #output_from_sw(output_from_SWv2, payload)

            else:
                pass

create_payload()
output_result.close()
