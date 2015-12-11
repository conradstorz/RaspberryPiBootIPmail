# RaspberryPiBootIPmail
Python script to send an email on boot

Save this script using a nice name like 'startup_mailer.py' and make note of its path (like /home/pi/Code/startup_mailer.py)

For good measure, make the script executable

sudo chmod +x startup_mailer.py

Edit /boot/boot.rc

Using your text editor once again, edit /boot/boot.rc (this assumes you have already renamed this file to boot.rc If not, see RPi_Advanced_Setup). For example:

sudo nano /boot/boot.rc

Add the following at the end of the file, making changes to the path for your directory tree and save.

python /home/pi/Code/startup_mailer.py

Alternative if Using Rasbian

If you are using Rasbian you won't have a /boot/boot.rc file. Instead you can edit /etc/rc.local as follows:

 sudo nano /etc/rc.local

Add the 'python /home/pi/Code/startup_mailer.py' line, so the file now looks like this:

 # rc.local
 #
 # This script is executed at the end of each multiuser runlevel.
 # Make sure that the script will "exit 0" on success or any other
 # value on error.
 #
 # In order to enable or disable this script just change the execution
 # bits.
 #
 # By default this script does nothing.
 # Print the IP address if it doesn't work ad sleep 30 before all your code 
 _IP=$(hostname -I) || true
 if [ "$_IP" ]; then
   printf "My IP address is %s\n" "$_IP"
   python /home/pi/Code/startup_mailer.py        <<<------------------------------------------ ADD THIS LINE!!!
 fi
 exit 0

FINISHED!

Reboot your Pi and you should receive an email with your ip address.
Troubleshooting

+ If you don't get your email notification: connect your pi to a monitor, boot and wait until you reach the 'login' prompt, and check if it says "My IP Address is...". If it doesn't, you may add 'sleep 30'(no quotes) in the etc/rc.local just after the last comment(# Print the IP...).

+ If you don't get email when rebooting, you have to check the hostname you currently have. because the script calls for #raspberrypi. Just type in the command line # hostname. if you have an other hostname its simple just change you hostname #with your preferred editor. Also in etc/hosts on the bottom of the page.

$ msg['Subject'] = 'IP For YOUR HOSTNAME on %s' % today.strftime('%b %d %Y') 
