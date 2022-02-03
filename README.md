# The CoM Network Automation Repo

This is a series of network automation scripts written in [Python](https://www.python.org/) which lean heavily on the [Nornir](https://github.com/nornir-automation/nornir) framework to automate some basic tasks.

So far, there are three functional scripts - a configuration backup tool, a password reset script, and a MAC address finder.

I have included a sample inventory so you have a starting point, but my inventory is bare bones and you can do a lot more with it.  I suggest starting here for more info: [Nornir Inventory Tutorial](https://nornir.readthedocs.io/en/latest/tutorial/inventory.html)

If you have suggestions or see glaring issues please feel free to critique the implementation.

## GETTING STARTED

Using the scripts as-is will require creating an inventory folder (or renaming the 'sample_inventory' folder to simply 'inventory'), and adding some of your actual devices and credentials to the **hosts.yaml** and **defaults.yaml** files. You could instead add functionality to the scripts to allow for alternative access to this information.

## Notes about 'com_sec' and 'com_uc'

'com_sec' and 'com_uc' are basically just stub projects at this point - 'com_sec' is for security related scripting, and 'com_uc' is for automation scripts related to our VoIP systems.  I have a few working scripts throughout those folders, but they are borrowed/modified from elsewhere or mostly just sample ideas. I claim no authorship of these files, and have them included here simply due to the convience of having everything related to automation in one workspace.
