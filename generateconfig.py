import getpass
from passlib.hash import md5_crypt

#Methods
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

#Get Variables
hostname = raw_input("Enter desired Hostname: ")

management_IP = raw_input("Enter desired Management IP: ")

print "Enter desired GAIA password"
password = getpass.getpass()
print "Enter desired GAIA password again"
password2 = getpass.getpass()
if 

print "Enter desired SIC Key"
sic_key = getpass.getpass()

dns_IP = raw_input ("Enter Desired DNS Server(Optional - Default is 8.8.8.8): ")
if dns_IP is "":
	dns_IP = "8.8.8.8"
    
#Generate Admin Password Hash
hash = md5_crypt.encrypt(password)



replace_line('firstconfig.conf', 73, 'mgmt_admin_passwd=' + password + "\n")
replace_line('firstconfig.conf', 101, 'ftw_sic_key=' + sic_key  + "\n")
replace_line('firstconfig.conf', 121, "admin_hash='" + hash  + "'\n")
replace_line('firstconfig.conf', 140, "management_IP='" + hash  + "'\n")
replace_line('firstconfig.conf', 150, "hostname=" + hostname  + "\n")
replace_line('firstconfig.conf', 171, "primary=" + dns_IP  + "\n")
