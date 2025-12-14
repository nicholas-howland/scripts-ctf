# HTB Writeup

## Objective
What is the content of the hidden .txt file in the web folder?
What is the name of the suspicious process?
What is the service name affiliated with the suspicious process?
What is the log file name of the miner instance?
What is the wallet address of the miner instance?
The wallet address used has been involved in transactions between wallets belonging to which threat group?

## Scope
10.10.217.148

## Steps Taken
- Went to the main page and was greeted with the picture of a brick wall.
- Noticed a file in the zap log called 404.txt which brought me to 404 page with a search box.
- After playing around with the website and completing a spider of the known pages I looked up the content management system. The bricks plugin had a disclosed CVE-2024-25600 which allows for remote code execution for unauthenticated users.
- I found a handy exploit tool created by Chocapikk which allows for the execution of php code on the host. Why this is dangerous is because php allows for operating system commands to be executed server side. His repo can be found here: https://github.com/Chocapikk/CVE-2024-25600.
- I had issues getting the webshells to work properly, but meterpreter did not fail to get some code remotely executing on the server. There was an issue with getting a reliable shell set up through meterpreter though so a webshell by WhiteWinterWolf was used.
- After looking through the running commands with `ps` no suspicious processess were found. Next the services were checked to see if there were any suspicious services running. A service named `TRYHACK3M` was running associated with the service `ubuntu.service`.
- The ubuntu.service file could be found in the following directories:
```
/sys/fs/cgroup/devices/system.slice/ubuntu.service
/sys/fs/cgroup/memory/system.slice/ubuntu.service
/sys/fs/cgroup/cpu,cpuacct/system.slice/ubuntu.service
/sys/fs/cgroup/pids/system.slice/ubuntu.service
/sys/fs/cgroup/blkio/system.slice/ubuntu.service
/sys/fs/cgroup/systemd/system.slice/ubuntu.service
/run/systemd/units/invocation:ubuntu.service
/sys/fs/cgroup/unified/system.slice/ubuntu.service
/etc/systemd/system/multi-user.target.wants/ubuntu.service
/etc/systemd/system/ubuntu.service
```
- The executable it was pointing to was named `/lib/NetworkManager/nm-inet-dialog` with a md5 hash of `2d96bf6e392bbd29c2d13f6393410e4599a40e1f2fe9dc8a7b744d11f05eb756` in virus total it was classified as a miner.python/syzkv.
- After pulling the malware/miner down and talking a look at it in GHIDRA it looks like they took some anti debugging measures, splitting up functions, etc...
- After looking at the dropped files in virustotal
- I looked at processes and the service that it was being run under and did not find any kind of command line option that was pointing to a log file.
- I went ahead and tried to run the file because I was out of options on the compromised machine. It spit out an error:
`TERM environment variable not set.`
- This means that the mainer is using environment variubles to set the locations of files.
- I tried to kill the new instance and it looks like the threat actor enabled a feature to start another mining process in the background after attempting to kill the process. This could be why there are two processes started when the program is executed.
- Note when running the dirty pipe exploit aka DirtyPipe the library /lib/x86_64-linux-gnu/libc.so.6 is required

### I broke down
- By using the writeup here I was able to find the hint I needed to continue to complete this shit in a reasonable time. https://medium.com/@timnik/tryhack3m-bricks-heist-a0768e9615bf
- Once locating the log in the hosted directory of the cryptominer, /lib/NetworkManager/init.conf, A line of encoded text revealed the bitcoin wallet address of bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa
- To find the threat group associated with the wallets the above wallet was transacting to i searched the following wallets
- One of the first transactions made from the wallet was from bc1q5jqgm7nvrhaw2rh2vk0dk8e4gg5g373g0vz07r which according to an OFAC press release was added to the SDN lists https://ofac.treasury.gov/recent-actions/20240220





## Output
```
ubuntu      2107  0.0  0.6 344220 27000 ?        Sl   Jun24   0:00 nm-applet
apache      3050  0.0  0.0   2616   596 ?        S    01:48   0:00 sh -c cd '/data/www/default' ; exec 2>&1; /lib/NetworkManager/nm-inet-dialog
apache      3051  0.0  0.0   2820   652 ?        S    01:48   0:00 /lib/NetworkManager/nm-inet-dialog
apache      3052  0.2  0.6  34808 27828 ?        S    01:48   0:00 /lib/NetworkManager/nm-inet-dialog
root        3056  0.1  0.0   2820   648 ?        Ss   01:48   0:00 /lib/NetworkManager/nm-inet-dialog
root        3057  0.2  0.7  34808 28204 ?        S    01:48   0:00 /lib/NetworkManager/nm-inet-dialog
apache      3068  0.0  0.0   2616   596 ?        S    01:49   0:00 sh -c cd '/data/www/default' ; exec 2>&1; ps aux | grep nm-
apache      3070  0.0  0.0   8168   724 ?        S    01:49   0:00 grep nm-
```
Linpeas possible root exploit
```
[CVE-2022-2586] nft_object UAF[0m

   Details: https://www.openwall.com/lists/oss-security/2022/08/29/5
   Exposure: probable
   Tags: [ ubuntu=(20.04) ]{kernel:5.12.13}
   Download URL: https://www.openwall.com/lists/oss-security/2022/08/29/5/1
   Comments: kernel.unprivileged_userns_clone=1 required (to obtain CAP_NET_ADMIN)

[+] [1;31m[CVE-2022-0847] DirtyPipe[0m

   Details: https://dirtypipe.cm4all.com/
   Exposure: probable
   Tags: [ ubuntu=(20.04|21.04) ],debian=11
   Download URL: https://haxx.in/files/dirtypipez.c

[+] [1;31m[CVE-2021-4034] PwnKit[0m

   Details: https://www.qualys.com/2022/01/25/cve-2021-4034/pwnkit.txt
   Exposure: probable
   Tags: [ ubuntu=10|11|12|13|14|15|16|17|18|19|20|21 ],debian=7|8|9|10|11,fedora,manjaro
   Download URL: https://codeload.github.com/berdav/CVE-2021-4034/zip/main

[+] [1;31m[CVE-2021-3156] sudo Baron Samedit[0m

   Details: https://www.qualys.com/2021/01/26/cve-2021-3156/baron-samedit-heap-based-overflow-sudo.txt
   Exposure: probable
   Tags: mint=19,[ ubuntu=18|20 ], debian=10
   Download URL: https://codeload.github.com/blasty/CVE-2021-3156/zip/main

[+] [1;31m[CVE-2021-3156] sudo Baron Samedit 2[0m

   Details: https://www.qualys.com/2021/01/26/cve-2021-3156/baron-samedit-heap-based-overflow-sudo.txt
   Exposure: probable
   Tags: centos=6|7|8,[ ubuntu=14|16|17|18|19|20 ], debian=9|10
   Download URL: https://codeload.github.com/worawit/CVE-2021-3156/zip/main

[+] [1;31m[CVE-2021-22555] Netfilter heap out-of-bounds write[0m

   Details: https://google.github.io/security-research/pocs/linux/cve-2021-22555/writeup.html
   Exposure: probable
   Tags: [ ubuntu=20.04 ]{kernel:5.8.0-*}
   Download URL: https://raw.githubusercontent.com/google/security-research/master/pocs/linux/cve-2021-22555/exploit.c
   ext-url: https://raw.githubusercontent.com/bcoles/kernel-exploits/master/CVE-2021-22555/exploit.c
   Comments: ip_tables kernel module must be loaded

[+] [1;31m[CVE-2022-32250] nft_object UAF (NFT_MSG_NEWSET)[0m

   Details: https://research.nccgroup.com/2022/09/01/settlers-of-netlink-exploiting-a-limited-uaf-in-nf_tables-cve-2022-32250/
https://blog.theori.io/research/CVE-2022-32250-linux-kernel-lpe-2022/
   Exposure: less probable
   Tags: ubuntu=(22.04){kernel:5.15.0-27-generic}
   Download URL: https://raw.githubusercontent.com/theori-io/CVE-2022-32250-exploit/main/exp.c
   Comments: kernel.unprivileged_userns_clone=1 required (to obtain CAP_NET_ADMIN)

[+] [1;31m[CVE-2017-5618] setuid screen v4.5.0 LPE[0m

   Details: https://seclists.org/oss-sec/2017/q1/184
   Exposure: less probable
   Download URL: https://www.exploit-db.com/download/https://www.exploit-db.com/exploits/41154\
```
# Additional Information



