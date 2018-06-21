import getpass
import time
import paramiko
    
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


'''Prompt User to check blades'''

#Login to management API
rc.send("expert")
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)

rc.send("mgmt_cli login -r true session-name PyConfig ")
rc.send("\n")
time.sleep(1)
rc.send(password)
rc.send("\n")
time.sleep(2)


'''Check to see if Management API is Enabled'''

#Create FW_Layer and Rule
rc.send("lock database override")
rc.send("\n")

time.sleep(2)
rc.send('mgmt_cli -r true add access-layer name FW_Layer firewall true ')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true  add access-rule layer FW_Layer position 1 name Accept_All action Accept destination Any source Any enabled true track none')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true delete access-rule name "Cleanup rule" layer FW_Layer ')
rc.send("\n")
time.sleep(2)

#Create APP&URLF Layer and Rule
rc.send("mgmt_cli -r true add access-layer name APP&URLF applications-and-url-filtering true firewall false ")
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true add access-rule layer APP&URLF position 1 name Content_Logging action Accept source Any destination Internet data "Any File" data-direction up track "detailed log" enabled true ')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true add access-rule layer APP&URLF position 2 name APPLC_Logging action Accept source Any destination Internet track "detailed log" enabled true ')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true set package name Standard access-layers.add.1.name "APP&URLF" access-layers.add.1.position 2')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true delete access-rule name "Cleanup rule" layer APP&URLF')
rc.send("\n")
time.sleep(2)      

#Publish Rules
rc.send('mgmt_cli -r true publish ')
rc.send("\n")
time.sleep(10)
rc.send('mgmt_cli -r true  install-policy policy-package "Standard" ')
rc.send("\n")
time.sleep(25)
rc.send('mgmt_cli -r true "')
rc.send("\n")
results = rc.recv(8000)
print results
