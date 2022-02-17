# The City of Mentor MAC Address Finder
# Written by Dan King
# Last update: 02/17/2022
# 
# TODO: Currently, MAC addresses must be entered in the form of 0000.0000.0000 (or any form Cisco will read, but the preference is the format shown here.)
# Must implement code to change any format of MAC address to 0000.0000.0000 before sending to devices.

import re
import logging
import csv
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F

nr = InitNornir(
    config_file="com_nornir/config.yaml")

def get_mac_addr():
    #mac_addr = input("Enter a MAC address please: ")
    mac_addr = '94D4.692A.FDB8'
    # After entering a MAC address, the following lines create a copy of the address with all punctuation removed.  We use this to compare to the search results later. 
    mac_addr_mod = mac_addr.replace(":","")
    mac_addr_mod = mac_addr_mod.replace("-","")
    mac_addr_mod = mac_addr_mod.replace(".","")
    mac_addr_mod = mac_addr_mod.lower()
    find_mac_addr(mac_addr, mac_addr_mod)

def find_mac_addr(mac_addr, mac_addr_mod):
    logging.info("MAC needed is: " + mac_addr)
    # The below line is here in case you want to run against just the test group.  Make sure a device is added to this group in the hosts.yaml file.
    nr_filter = nr.filter(F(groups__contains="co"))
    # If you do run against the test group above, you need to change the below line so "nr.run" is instead "nr_filter.run"
    output = nr_filter.run(task=netmiko_send_command,command_string="show mac address-table address " + str(mac_addr))
    logging.info(f'The value of output is: {str(output)}')
    for hostname in output:
        logging.info(f'Currently searching {str(hostname)}')
        string_needed = re.compile(
            r"[a-fA-F0-9]{4}.[a-fA-F0-9]{4}.[a-fA-F0-9]{4}")
        # logging.info("string_needed = " + str(string_needed))
        # logging.info("Output.result is " + output[hostname][0].result)
        mo = string_needed.search(output[hostname][0].result)
        # logging.info(f'The value of mo is {str(mo)}')
        try:
            mac_found = mo.group()
            mac_found = mac_found.replace(".", "")
            mac_found = mac_found.lower()
            logging.info(f'mac_found = {str(mac_found)}')
            logging.info(f'mac_addr_mod = {str(mac_addr_mod)}')
            # Below is where the modified MAC is compared to any matches found.
            if mac_found == mac_addr_mod:
                print(f'Match found on host {str(hostname)}:\n{output[hostname][0].result}')
                #print(f'Hostname is: {str(hostname)}\n')
                # TODO: Add a filter that looks for "Po" in the interface or port column, and if it finds it, skips to next device.
                # Until then, this will work but it will show all trunks the MAC is found on as well as the access interface
                #break

        except:
            logging.info(f'MAC address not found on host: {hostname}')


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s- %(levelname)s- %(message)s', filename='mac_finder.log')
    get_mac_addr()

if __name__ == "__main__":
    main()
