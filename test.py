#Written By Mike Braun
#Version 1.0

import getpass
import time
import paramiko
    
#Get Variables
print "Checkpoint Rule Configuration Script \n"
print "In order for this script to work, the management API has to be enabled. \n"

ip_address = raw_input("Enter Management IP: ")
username = raw_input("Enter GAIA username: ")
print "Enter GAIA password"
password = getpass.getpass()
policy_name = raw_input("Enter Policy Name: ")
#client_interface = raw_input("Enter Client Interface: ")
#monitor_interface = raw_input("Enter Monitor Interface: ")

#Establish SSH Connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect (ip_address, username=username, password=password)
rc = ssh.invoke_shell()

#Enter Expert Mode
rc.send("expert")
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)


#Login to management API
rc.send("mgmt_cli login -r true session-name PyConfig > /home/admin/id.txt ")
rc.send("\n")
time.sleep(3)


#Create FW_Layer and Rule
time.sleep(2)
rc.send('mgmt_cli -r true add access-layer name "FW_Layer" applications-and-url-filtering true content-awareness true firewall true')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true  add access-rule layer "FW_Layer" position 1 name Accept_All action Accept destination Any source Any enabled true track none')
rc.send("\n")
time.sleep(10)

#Create APP&URLF Rule

rc.send('mgmt_cli -r true add access-rule layer "FW_Layer" position 2 name Content_Logging action Accept source Any destination Internet data "Any File" data-direction up track "detailed log" enabled true')
rc.send("\n")
time.sleep(12)
rc.send('mgmt_cli -r true add access-rule layer "FW_Layer" position 3 name APPLC_Logging action Accept source Any destination Internet track "detailed log" enabled true')
rc.send("\n")
time.sleep(10)
rc.send("\n")
time.sleep(10)
rc.send('mgmt_cli -r true delete access-rule name "Cleanup rule" layer "FW_Layer" position 4')
rc.send("\n")
time.sleep(10)
rc.send('mgmt_cli -r true set package name ' + policy_name + ' access-layers.add.1.name "FW_Layer" access-layers.add.1.position 1  ')
rc.send("\n") 
time.sleep(2)