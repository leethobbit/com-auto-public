# The City of Mentor MAC Address Finder Version 2
# Written by Dan King
# Last update: 02/18/2022
# 
# TODO: Currently, MAC addresses must be entered in the form of 0000.0000.0000 (or any form Cisco will read, but the preference is the format shown here.)
# Must implement code to change any format of MAC address to 0000.0000.0000 before sending to devices.

import csv
import re
import logging
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F

nr = InitNornir(
    config_file="com_nornir/config.yaml")

def get_mac_addr():
    """Gets the MAC address to be hunted for, and creates a modified copy for comparison in later functions."""
    # mac_addr = input("Enter a MAC address please: ")
    with open('com_nornir/backups/in_mac_leftover.csv') as f:
        reader = csv.DictReader(f)
        # Creates a list of all MAC addresses from the csv file
        macs = [line['MAC_ADDR'] for line in reader]
    
    for macs in macs:
        mac_addr = macs
        logging.info(f'MAC address passed from txt file is: {mac_addr}')
        mac_addr_mod = mac_addr.replace(":","")
        mac_addr_mod = mac_addr_mod.replace("-","")
        mac_addr_mod = mac_addr_mod.replace(".","")
        mac_addr_mod = mac_addr_mod.lower()
        find_mac_addr(mac_addr, mac_addr_mod)

def find_mac_addr(mac_addr, mac_addr_mod):
    """Searches the selected devices (either all or a subgroup) for the given MAC address, and prints any match it finds."""
    # logging.info("MAC needed is: " + mac_addr)
    # Change nr_filter.run below to nr.run if you want to run against all devices instead of a group.
    nr_filter = nr.filter(F(groups__contains="fhq"))
    output = nr_filter.run(task=netmiko_send_command,command_string="show mac address-table address " + str(mac_addr))
    # logging.info(f'The value of output is: {str(output)}')
    for hostname in output:
        # logging.info(f'Currently searching {str(hostname)}')
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
            # logging.info(f'mac_found type = {type(mac_found)}')
            # logging.info(f'mac_addr_mod type = {type(mac_addr_mod)}')
            # Below is where the modified MAC is compared to any matches found.
            if mac_found == mac_addr_mod:
                logging.info(f'Match found on host {str(hostname)}:\n{output[hostname][0].result}')
                # This next part extracts the specific interface out of the results, and prints/writes to txt file just the interface
                interface_needed = re.compile(r"Gi[0-9]/[0-9]/[0-9]{1,2}")
                inf = interface_needed.search(output[hostname][0].result)
                inf = inf.group()
                logging.info(str(inf))
                with open('com_nornir/backups/phones_txt.txt', 'a') as f:
                    f.write(f'{str(mac_found)},{str(inf)},{str(hostname)}\n')
                    f.close()
        except:
            logging.info(f'MAC address not found on host: {hostname}')


def main():
    """Logging is set here, and then get_mac_addr() is called."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s- %(levelname)s- %(message)s', filename='mac_finder_v2.log')
    get_mac_addr()


if __name__ == "__main__":
    main()
