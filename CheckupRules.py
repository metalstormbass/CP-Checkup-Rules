#Written By Mike Braun
#Version 1.0

import getpass
import time
import paramiko
    
#Get Variables
print "Checkpoint Rule Configureation Script \n"
print "In order for this script to work, the management API has to be enabled. \n"

ip_address = raw_input("Enter Management IP: ")
username = raw_input("Enter GAIA username: ")
print "Enter GAIA password"
password = getpass.getpass()
client_interface = raw_input("Enter Client Interface: ")
monitor_interface = raw_input("Enter Monitor Interface: ")

#Establish SSH Connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect (ip_address, username=username, password=password)
rc = ssh.invoke_shell()

#Set Client Interface
rc.send("lock database override")
rc.send("\n")
rc.send('add dhcp client interface '+ client_interface)
rc.send("\n")
time.sleep(2)
rc.send('set interface ' + monitor_interface + '  state on comments "This is for internet access"')
time.sleep(15)
rc.send("\n")
rc.send('set interface ' + monitor_interface + ' monitor-mode "SPAN Port"')
time.sleep(5)
rc.send("\n")

#Enter Expert Mode
rc.send("expert")
rc.send("\n")
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)

#Modify Kernel as per checkup guide
rc.send('echo "fw_local_interface_anti_spoofing=0" >> $FWDIR/modules/fwkern.conf')
time.sleep(2)
rc.send('echo "fw_antispoofing_enabled=0" >> $FWDIR/modules/fwkern.conf')
time.sleep(2)
rc.send('echo "sim_anti_spoofing_enabled=0" >> $FWDIR/modules/fwkern.conf')
time.sleep(2)
rc.send('echo "fw_icmp_redirects=1" >> $FWDIR/modules/fwkern.conf')
time.sleep(2)
rc.send('echo "fw_allow_out_of_state_icmp_error=1" >> $FWDIR/modules/fwkern.conf')
time.sleep(2)
rc.send('echo "psl_tap_enable=1" >> $FWDIR/modules/fwkern.conf')
time.sleep(2)
rc.send('echo "fw_tap_enable=1" >> $FWDIR/modules/fwkern.conf')
time.sleep(2)

#Login to management API
rc.send("mgmt_cli login -r true session-name PyConfig ")
rc.send("\n")
time.sleep(3)

#Enable Blades
rc.send('''fw_name=$(mgmt_cli -r true show simple-gateways -f json| $CPDIR/jq/jq '.["objects"][].name')''')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true set simple-gateway name $fw_name firewall true application-control true url-filtering true ips true anti-bot true anti-virus true threat-emulation true content-awareness true --format json ignore-warnings true') 
rc.send("\n")
time.sleep(15)
        
#Delete Default Network Layer
rc.send('mgmt_cli -r true set access-rule name "Cleanup rule" layer "Network" action Accept destination Any source Any enabled true track none --format json ignore-warnings true')
rc.send("\n")
time.sleep(2)

#Create FW_Layer and Rule
time.sleep(2)
rc.send('mgmt_cli -r true add access-layer name "FW_Layer" firewall true ')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli -r true  add access-rule layer "FW_Layer" position 1 name Accept_All action Accept destination Any source Any enabled true track none')
rc.send("\n")
time.sleep(10)
rc.send('mgmt_cli -r true delete access-rule name "Cleanup rule" layer "FW_Layer" ')
rc.send("\n")
time.sleep(4)
rc.send('mgmt_cli -r true set package name "Standard" access-layers.add.1.name "FW_Layer" access-layers.add.1.position 1')
rc.send("\n")
time.sleep(2)

#Create APP&URLF Layer and Rule
rc.send('mgmt_cli -r true add access-layer name "APP&URLF" applications-and-url-filtering true content-awareness true firewall false')
rc.send("\n")
time.sleep(4)
rc.send('mgmt_cli -r true add access-rule layer "APP&URLF" position 1 name Content_Logging action Accept source Any destination Internet data "Any File" data-direction up track "detailed log" enabled true ')
rc.send("\n")
time.sleep(12)
rc.send('mgmt_cli -r true add access-rule layer "APP&URLF" position 2 name APPLC_Logging action Accept source Any destination Internet track "detailed log" enabled true ')
rc.send("\n")
time.sleep(10)
rc.send('mgmt_cli -r true set package name "Standard" access-layers.add.1.name "APP&URLF" access-layers.add.1.position 2')
rc.send("\n")
time.sleep(4)
rc.send('mgmt_cli -r true set access-rule name "Cleanup rule" layer "APP&URLF" action Accept destination Any source Any enabled true track none --format json ignore-warnings true')
rc.send("\n")
time.sleep(4)      


#Publish Rules
rc.send('mgmt_cli -r true publish ')
rc.send("\n")
time.sleep(10)
rc.send('mgmt_cli -r true  install-policy policy-package "Standard" ')
rc.send("\n")
time.sleep(25)
rc.send('mgmt_cli -r true logout"')
rc.send("\n")
time.sleep(2)
results = rc.recv(8000)
print results
