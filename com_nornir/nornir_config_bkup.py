# The City of Mentor Cisco Config Backup Utility
# Written by Dan King
# Last update: 02/18/2022

import os
import logging
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko import netmiko_send_command
from datetime import datetime, date, time
from nornir.core.filter import F

now = datetime.now()
time = now.strftime('%Y-%m-%d')

BACKUP_DIR = f'com_nornir/backups/{time}/'

nr = InitNornir(
    config_file="com_nornir/config.yaml")

# Use the following to connect to only a specific group of devices
# If you change this, you must change the .run method in get_netmiko_backups
# test = nr.filter(F(groups__contains="test"))

def create_backups_dir():
    """Creates a backup directory using today's today, if one doesn't exist."""
    logging.info('Checking if backup directory exists.')
    if not os.path.exists(BACKUP_DIR):
        logging.info('Creating backup directory.')
        os.mkdir(BACKUP_DIR)

def save_config_to_file(method, hostname, config):
    """Takes the config and writes it to a file, using hostname and date to name the file."""
    filename = f'{hostname}-{method}-{time}.cfg'
    with open(os.path.join(BACKUP_DIR, filename), "w") as f:
        f.write(config)
    logging.info(f'{str(hostname)} backup created successfully.')

def get_netmiko_backups():
    """Grabs the contents of 'show run' from each device in hosts.yaml and then pipes it to the save_config_to_file() function"""
    logging.info('Now collecting configuration files.')
    backup_results = nr.run(
        task=netmiko_send_command,
        command_string="show run"
        )
    for hostname in backup_results:
        logging.info(f'Currently backing up {str(hostname)}')
        save_config_to_file(
            method="netmiko",
            hostname=hostname,
            config=backup_results[hostname][0].result,
        )

def main():
    """Sets logging parameters, then creates a backup folder, and finally gets the configurations and saves them into the backup folder."""
    logging.basicConfig(level=logging.INFO,format='%(asctime)s- %(levelname)s- %(message)s',filename='config_bkup.log')
    logging.info('Starting program.')
    create_backups_dir()
    get_netmiko_backups()
    logging.info('Program completed successfully!')

if __name__ == "__main__":
    main()

# Old code for reference
# 
# get_napalm_backups()
# here = os.path.dirname(os.path.abspath(__file__))
# filename = os.path.join(here, 'config.yaml')
# Testing napalm I ran into some issues, decided to stick with netmiko as a result.
# def get_napalm_backups():
#     backup_results = nr.run(task=napalm_get, getters=["config"])

#     for hostname in backup_results:
#         config = backup_results[hostname][0].result["config"]["startup"]
#         save_config_to_file(method="napalm", hostname=hostname, config=config)

