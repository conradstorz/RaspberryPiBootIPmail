# /env/python
"""
Script to generate an email containing the current IP address

here is a code found on stackexchange to locate the IP of the running instance
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
print(s.getsockname()[0])
s.close()

and another...
>>> import socket, struct, fcntl
>>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> sockfd = sock.fileno()
>>> SIOCGIFADDR = 0x8915
>>>
>>> def get_ip(iface = 'eth0'):
...     ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
...     try:
...         res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
...     except:
...         return None
...     ip = struct.unpack('16sH2x4s8x', res)[2]
...     return socket.inet_ntoa(ip)
... 
>>> get_ip('eth0')
'10.80.40.234'
>>> 


and yet another...
You can use the netifaces module. Just type:

easy_install netifaces
in your command shell and it will install itself on default Python installation.

Then you can use it like this:

from netifaces import interfaces, ifaddresses, AF_INET
for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    print '%s: %s' % (ifaceName, ', '.join(addresses))
On my computer it printed:

{45639BDC-1050-46E0-9BE9-075C30DE1FBC}: 192.168.0.100
{D43A468B-F3AE-4BF9-9391-4863A4500583}: 10.5.9.207

"""

__author__ = 'Cody Giles'
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "1.0"
__maintainer__ = "Cody Giles"
__status__ = "Production"

import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime

def connect_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type

# Change to your own account information
# Account Information
mail_to = 'conradstorz@gmail.com' email to send to.
gmail_user = 'estorz@gmail.com' # Email to send from. (MUST BE GMAIL)
gmail_password = 'zrsmxrlimdzvzhqb' # Gmail application specific password
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)  # Log in to server
today = datetime.date.today()  # Get current time/date

arg='ip route list'  # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()  # Get data from 'p terminal'.

# Split IP text block into three, and divide the two containing IPs into words.
ip_lines = data[0].splitlines()
split_line_a = ip_lines[1].split()
split_line_b = ip_lines[2].split()

# con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
ip_type_a = connect_type(split_line_a)
ip_type_b = connect_type(split_line_b)

"""Because the text 'src' is always followed by an ip address,
we can use the 'index' function to find 'src' and add one to
get the index position of our ip.
"""
ipaddr_a = split_line_a[split_line_a.index('src')+1]
ipaddr_b = split_line_b[split_line_b.index('src')+1]

# Creates a sentence for each ip address.
my_ip_a = 'Your %s ip is %s' % (ip_type_a, ipaddr_a)
my_ip_b = 'Your %s ip is %s' % (ip_type_b, ipaddr_b)

# Creates the text, subject, 'from', and 'to' of the message.
msg = MIMEText(my_ip_a + "\n" + my_ip_b)
msg['Subject'] = 'IPs For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = mail_to
# Sends the message
smtpserver.sendmail(gmail_user, [to], msg.as_string())
# Closes the smtp server.
smtpserver.quit()
