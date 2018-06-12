import getpass
import pip
import time

#Check if Paramiko is installed and install it if not.
try:
    import paramiko
except: 
    pip.main(['install', paramiko])
    
#Get Variables
ip_address = raw_input("Enter Management IP: ")

username = raw_input("Enter GAIA username: ")

print "Enter GAIA password"
password = getpass.getpass()

#Establish SSH Connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect (ip_address, username=username, password=password)
rc = ssh.invoke_shell()



#Login to management API
rc.send("mgmt login ")
rc.send("\n")
time.sleep(1)
rc.send(password)
rc.send("\n")
time.sleep(1)

'''Check to see if Management API is Enabled'''

#Create Rule
rc.send("lock database override")
rc.send("\n")
rc.send('mgmt_cli add package name "security_checkup" threat-prevention "false"')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli add access-layer name "FW_Layer"  firewall "true" add-default-rule "false" shared "true"')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli set package name "security_checkup" access-layers.add.1.name "FW_Layer" access-layers.add.1.position 1')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli add access-rule layer "FW_Layer" source "any" destination "any" service "any" action "accept" position "1" name "Accept All"')
rc.send("\n")
time.sleep(2)

#Publish Rules
rc.send('mgmt_cli publish')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli install-policy policy-package "security_checkup"')
rc.send("\n")

results = rc.recv(4000)
print results