
## Raspi e-mail
Script for sending IP address whenever raspberry pi boots and has IP address assigned.

RaspberryPi should have some of these fiels to configure startup scripts:
* `/boot/boot.rc`
* `/etc/rc.local`

```bash
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
	python /path/to/reportip.py        <<<---------------- ADD THIS LINE
fi

exit 0
```