# The City of Mentor Network Device Password Changer
# Written by Dan King
# Last update: 06/03/2021
#
# This script can be used to change the password of whichever user account is entered when prompted.
# It also automatically updates the 'defaults.yaml' file.
#
# This script will change the password on all hosts listed in the hosts.yaml file unless you designate a filter group - an example can be seen below.

import logging
from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir.core.filter import F
from ruamel.yaml import YAML

nr = InitNornir(
    config_file="com_nornir/config.yaml")

# Currently testing with a filter so only devices with 'pswd_test' as their group will be used
pswd_test = nr.filter(F(groups__contains="pswd_test"))

def update_defaults_pswd(new_pswd):
    # This function updates the defaults.yaml file with the new password
    yaml = YAML()
    yaml.explicit_start = True
    yaml.preserve_quotes = True

    file_name = 'com_nornir/inventory/defaults.yaml'
    with open(file_name) as fp:
        data = yaml.load(fp)

    data['password'] = new_pswd

    with open(file_name, 'w') as fp:
        yaml.dump(data, fp)
        
    logging.info(f'Password has been updated in the defaults.yaml file!')

def send_new_pswd_to_devices(username,new_pswd):
    # This function sends new password to all network devices (or a subset if using a group filter)
    pswd_test.run(task=netmiko_send_config, config_commands=f'username {username} privilege 15 password {new_pswd}')
    logging.info(f'Password has been successfully changed for user {username}!')
    # TODO: Should do some sort of verification once password is changed.
    update_defaults_pswd(new_pswd)

def create_new_pswd():
    username = input("Please enter the username to modify: ")
    new_pswd = input("Please enter a new password: ")
    logging.info(f'The username you entered is: {username}')
    logging.info(f'The new password you entered is: {new_pswd}')
    send_new_pswd_to_devices(username,new_pswd)

def main():
    # This enables logging of INFO level events.  This will be chatty but not nearly as much as DEBUG mode would.
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', filename='pswd_reset.log')
    create_new_pswd()

if __name__ == "__main__":
    main()
