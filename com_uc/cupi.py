import requests

# Function to validate Cisco server application is accessable
def server_check(server):
    try:
        reply = requests.get("https://{}:8443/".format(server), verify=False, timeout=3)
    # Test if server application is accessable within 3 seconds
    except requests.exceptions.RequestException:
        return False
    # If server check receives valid "200" response, break out of iteration
    else:
        if reply.status_code == 200:
            return True
        else:
            return False

# Function to check if UCXN user is valid and return user object ID
def user_check(server, acct, pw, user, pin):
    url = "https://{}/vmrest/users?query=(alias is {})".format(server, user)
    try:
        reply = requests.get(url, auth=(acct, pw), verify=False, headers={"Accept":"application/json"})
    # User request error
    except requests.exceptions.RequestException as err:
        return {"error": err}
    # Return values based on request response
    else:
        if reply.status_code == 200:
            # Pull total users from JSON reply
            if reply.json()['@total'] == "1":
                obj_id = reply.json()["User"]["ObjectId"]
                return {"success": obj_id}
            else:
                return {"error": "User Not In System"}
        elif reply.status_code == 401:
            return {"error": "Server Credential Error"}
        elif reply.status_code == 404:
            return {"error": "No Users Found"}
        else:
            return {"error": "Unknown Result"}

# Function to set UCXN user pin based on passed object ID and pin
def pin_set(server, acct, pw, obj_id, pin):
    url = "https://{}/vmrest/users/{}/credential/pin".format(server, obj_id)
    data = {'Credentials': pin}
    try:
        reply = requests.put(url, auth=(acct, pw), verify=False, json=data, headers={"Accept":"application/json", "Content-Type":"application/json"})
    # Check for error
    except requests.exceptions.RequestException as err:
        return err
    # Return values based on request response
    else:
        if reply.status_code == 204:
            return "Pin Successfully Reset"
        elif reply.status_code == 400: # Return exact error message from UCXN
            return reply.json()["errors"]["message"]
        else:
            return "Unknown Result - Double Check Values"