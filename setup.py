import getpass
import time
import paramiko
import serial
from passlib.hash import md5_crypt
from scp import SCPClient


#Get Variables
serial_port = "Enter COM Port (Ex: COM5): "

hostname = raw_input("Enter desired Hostname: ")

management_IP = raw_input("Enter desired Management IP: ")

username = raw_input("Enter GAIA username: ")

print "Enter desired GAIA password"
password = getpass.getpass()

print "Enter desired Expert Password"
expert_password = getpass.getpass()

print "Enter desired SIC Key"
sic_key = getpass.getpass()

client_IP = raw_input ("Enter desired Client IP(Optional): ")
if client_IP is "":
	client_interface = raw_input ("Enter desired Client Interface(Default is eth5): ")
	if client_interface is "":
		client_interface = "eth5"

dns_IP = raw_input ("Enter Desired DNS Server(Optional - Default is 8.8.8.8): ")
if dns_IP is "":
	dns_IP = "8.8.8.8"

license_string = raw_input ("Enter License String (Do not include cplic put): ")

contract_location = raw_input("Enter full path to ServiceContract.xml (including filename): ")
       
    
 '''First time Config Wizard Stuff Here''' 
#Generate Admin Password Hash
hash = md5_crypt.encrypt(password)

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

replace_line('first.conf', 73, 'mgmt_admin_passwd=' + password + "\n")
replace_line('first.conf', 101, 'ftw_sic_key=' + sic_key  + "\n")
replace_line('first.conf', 121, "admin_hash='" + hash  + "'\n")
replace_line('first.conf', 140, "admin_hash='" + hash  + "'\n")
replace_line('first.conf', 150, "hostname=" + hostname  + "\n")
replace_line('first.conf', 171, "primary=" + dns_IP  + "\n")

#Establish Serial Connection
ser = serial.Serial(serial_port, 9600)

#USE SUBPROCESS TO CAT FIRST.CONF AND ASSIGN TO VARIABLE

#Login
ser.write("admin")
ser.write("\n")
time.sleep(1)
ser.write("admin")
ser.write("\n")
time.sleep(2)

ser.write("set expert-password")
ser.write("\n")
time.sleep(1)
ser.write(expert_password)
ser.write("\n")
time.sleep(1)
ser.write(expert_password)


#Close Serial Connection
ser.close()
    
    
    
    
#Establish SSH Connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect (ip_address, username=username, password=password)
rc = ssh.invoke_shell()

#Configure Interface
rc.send("lock database override")
rc.send("\n")


rc.send('add dhcp client interface '+ client_interface)
rc.send("\n")
time.sleep(2)
rc.send('set interface ' + client_interface + ' state on')
time.sleep(15)
rc.send("\n")

#Activate License
rc.send("lock database override")
rc.send("\n")
rc.send("cplic put '"+ license_string + "'")
rc.send("\n")


#Set to Expert for contract install
rc.send('expert')
rc.send('\n')
time.sleep(2)
rc.send(password)
rc.send("\n")
time.sleep(2)

#Upload Contract File
scpclient.put(contract_location, "/var/log")

#Activate Contract

rc.send("cplic contract put -o /var/log/ServiceContract.xml") 
rc.send("\n")
time.sleep(2)


'''Prompt User to check blades'''

#Login to management API
rc.send("mgmt login ")
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
rc.send('mgmt_cli add access-layer name FW_Layer firewall true')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli add access-rule layer FW_Layer position 1 name Accept_All action Accept destination Any source Any enabled true track none')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli delete access-rule name "Cleanup rule" layer FW_Layer')
rc.send("\n")
time.sleep(2)

#Create APP&URLF Layer and Rule
rc.send("mgmt_cli add access-layer name APP&URLF applications-and-url-filtering true firewall false")
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli add access-rule layer APP&URLF position 1 name Content_Logging action Accept source Any destination Internet data "Any File" data-direction up track "detailed log" enabled true')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli add access-rule layer APP&URLF position 2 name APPLC_Logging action Accept source Any destination Internet track "detailed log" enabled true')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli set package name Standard access-layers.add.1.name "APP&URLF" access-layers.add.1.position 2')
rc.send("\n")
time.sleep(2)
rc.send('mgmt_cli delete access-rule name "Cleanup rule" layer APP&URLF')
rc.send("\n") 
time.sleep(2)
        

#Publish Rules
stdin, stdout, stderr = rc.exec_command('mgmt_cli publish')
exit_status = stdout.channel.recv_exit_status()
if exit_status == 0:
    print ("Policy Published")
else:
    print("Error", exit_status)
stdin, stdout, stderr = rc.exec_command('mgmt_cli install-policy policy-package "Standard"')
exit_status = stdout.channel.recv_exit_status()
if exit_status == 0:
    print ("Policy Installed")
else:
    print("Error", exit_status)

rc.send('logout"')
rc.send("\n")
results = rc.recv(8000)
print results
