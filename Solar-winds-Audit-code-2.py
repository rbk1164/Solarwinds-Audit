# Author: ROHIT KADAM
################################ Extracting list of all the hosts present in the file ################################

import requests
import json
import subprocess as sp

file_input1 = input("Please enter path of the csv file:")
fp1 = open('{}'.format(file_input1),'r')   #####Book1 is csv file exported from itfs web

file_input2 = input("Please enter path of csv file where you want your new info:")
fp2 = open('{}'.format(file_input2),'w')

def create_list_of_devices():    ### create list of devices from csv file
    read_csv = fp1.read()
    csv_to_list1 = read_csv.split('\n')
    #print (y)

    for item in csv_to_list1:      #### remove empty fields
        if len(item) == 0:
            y.pop(y.index(item))

    csv_to_list2 = []
    for item in csv_to_list1:
        csv_to_list2.append(item.split(','))     #In case sometimes in the output you see /t instead of ',' replace ',' with '/t' in this line
    dev_list=[]
    for device in csv_to_list2:
        dev_list.append(device[0])       #take first element from every item present in list z

    dev_list.remove('Hostname')
    return(dev_list)



###################### adding only fpi, rpi and spi devices to a new-list ################################
new_devices = []
all_device = create_list_of_devices()
for device in all_device:
    if 'rpi' in device:
        new_devices.append(device)
    elif 'spi' in device:
        new_devices.append(device)
    elif 'fpi' in device:
        new_devices.append(device)
    else:
        pass
print (new_devices)



################################## Creating functions for ip, dns and ping and adding to the list ############################

new_csv = "Hostname,IP,DNS,Ping\n"

fp2.write(new_csv)

def ping(device):
    status,result = sp.getstatusoutput("ping -n 2 -w 2 " + str(device))
    print (result)

    if "unreachable" in result:
        return 'unreachable'
        #print("System " + str(device) + " is UNREACHABLE !")

    elif status == 0:
        return 'alive'
        #print("System " + str(device) + " is UP !")
        #l.append(device)
    else:
        return 'dead'
        #print ("System " + str(device) + " is DOWN !")

def nslookup():
    sw_dev = []    ####creating list to add to solarwinds
    for device in new_devices:
        result = sp.getstatusoutput("nslookup " + str(device))
        x=(list(result[1]))
        y=result[1].split()
        if y[5] == 'Non-existent':
            pass
        else:
            ping_status = ping(device)
            fp2.write(",".join([device, y[9], y[7], ping_status,"\n"]))
            if ping_status == "alive":
                sw_dev.append(device)


    fp2.close()
    return sw_dev
    
########################### Making get request to solarwinds API##############################

sw_dev1 = nslookup()

sw_dev2 = ','.join(sw_dev1)
headers = {'NetOps-API-Key': ''}

get = requests.get("http://solarwinds-server".format(sw_dev2), headers=headers)

q = get.json()

add_to_sw=[]
for item in q["output"]:
    if item["status_code"] == 404:
        add_to_sw.append(item["object"])
    else:
        pass
        #r.append(q.index(item))
print ("List of devices to be added to SolarWinds:\n",add_to_sw)
print ("\n")
#print ("No. of devices not present in NB:\n",len(k))

fp1.close()
