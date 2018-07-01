import getpass
import serial
import time

#Method
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

#Get Variables

serial_port = raw_input("Enter COM Port (Ex: COM5): ")

hostname = raw_input("Enter desired Hostname: ")

management_IP = raw_input("Enter desired Management IP: ")

while True:

    print "Enter desired GAIA password"
    password = getpass.getpass()
    print "Enter desired GAIA password again"
    password2 = getpass.getpass()
    if password == password2:
        break
    else:
        print "Problem Occured. Please re-enter your password.\n"

dns_IP = raw_input ("Enter Desired DNS Server(Optional - Default is 8.8.8.8): ")
if dns_IP is "":
	dns_IP = "8.8.8.8"
    
replace_line('firstconfig.conf', 43, 'mgmt_admin_passwd=' + password + "\n")
replace_line('firstconfig.conf', 44, "ipaddr_v4=" + management_IP  + "\n")
replace_line('firstconfig.conf', 45, "hostname=" + hostname  + "\n")
replace_line('firstconfig.conf', 46, "primary=" + dns_IP  + "\n")
 
#Establish Serial Connection
ser = serial.Serial(serial_port, 9600)

#Login
ser.write("admin")
ser.write("\n")
time.sleep(2)
ser.write("admin")
ser.write("\n")
time.sleep(2)

#Change Password
ser.write("set selfpasswd")
ser.write("\n")
time.sleep(1)
ser.write("admin")
ser.write("\n")
time.sleep(1)
ser.write(password)
ser.write("\n")
time.sleep(1)
ser.write(password)
ser.write("\n")
time.sleep(1)

#Set Expert Password
ser.write("set expert-password")
ser.write("\n")
time.sleep(1)
ser.write(password)
ser.write("\n")
time.sleep(1)
ser.write(password)
ser.write("\n")
time.sleep(1)

#Expert
ser.write("expert")
ser.write("\n")
time.sleep(2)
ser.write(password)
ser.write("\n")
time.sleep(2)

#Create Configuration File and Run
f = open('firstconfig.conf', "r")
line = f.readline()
num = 1
while line:
    ser.write('echo "' + line + '" >> ./firstconfig.conf')
    ser.write("\n")
    time.sleep(1)
    line = f.readline()
    print num
    num = num + 1
f.close()


ser.write("config_system -f ./firstconfig.conf")
ser.write("\n")
time.sleep(1)
ser.close()


print "First Time Wizard Running. Serial Connection Disconnected"