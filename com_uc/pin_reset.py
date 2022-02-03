from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from getpass import getpass
from cupi import server_check, user_check, pin_set

if __name__ == "__main__":

    # Disable certificate warnings
    disable_warnings(InsecureRequestWarning)

    while True:
        # Input UCXN IP address
        server = input("UCXN IP Address (Q to quit): ")
        # Allow option to quit
        if server == "Q" or server == "q":
            break
        else:
            # Validate server is reachable
            if not server_check(server):
                print("{} Unreachable".format(server))
            else:
                # Collect server credentials
                acct = input("UCXN ID: ")
                pw = getpass("UCXN PW: ")
                # Collect user information
                user = input("User to Update: ")
                pin = input("Non-Trivial Pin: ")
                # Call function to validate user and collect user object ID
                user_result = user_check(server, acct, pw, user, pin)
                if "error" in user_result:
                    print(user_result["error"])
                else:
                    # Call function to reset pin based on user object ID
                    obj_id = user_result["success"]
                    print(pin_set(server, acct, pw, obj_id, pin))
