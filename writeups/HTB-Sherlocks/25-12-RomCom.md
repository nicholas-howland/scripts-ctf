## Rom Com Sherlock
This is my writeup for the RomCom Sherlock from Hack The Box. This box has an official writeup released which can be found on the challenge page which can be found here: [RomCom](https://app.hackthebox.com/sherlocks/RomCom) 

## Narrative
Susan works at the Research Lab in Forela International Hospital. A Microsoft Defender alert was received from her computer, and she also mentioned that while extracting a document from the received file, she received tons of errors, but the document opened just fine. According to the latest threat intel feeds, WinRAR is being exploited in the wild to gain initial access into networks, and WinRAR is one of the Software programs the staff uses. You are a threat intelligence analyst with some background in DFIR. You have been provided a lightweight triage image to kick off the investigation while the SOC team sweeps the environment to find other attack indicators.

## Summary
Using a disk image from the provided password protected zip archive and details about when an initial compromise occured. I learned how to parse information from the Master File Table which is where windows will store details about file creation, deletion, and alteration on a partition. By analyzing these tables with a given a file name to discover malicious behavior. This scenario involves events related to the `RomCom` group's use of CVE-2025-8088. This CVE allowed for arbitrary code execution by unpacking a malicious `.rar` archive on unpatched versions of winrar.

ESET attributed RomCom to be a financially motivated criminal group operating from Russia [Ars Technica, Dan Goodin, Aug 2025](https://arstechnica.com/security/2025/08/high-severity-winrar-0-day-exploited-for-weeks-by-2-groups/) They have been known to use this CVE to get targets connected with their Mythic C2 framework. What is interesting about this is that the Mythic C2 framework does not provide payloads but instead allows for custom payload generation, meaning that the RomCom group had developed their own custom payload.

## How does COM Hijacking Work?
In short what will happen is a piece of malware will get introduced to a system via phishing, physical plant, etc. When it is executed by a user with the proper privilege set it will either overwrite a registry key to point to a malicious executable or overwrite other files to point to other payloads.

## Sherlock Questions and Answers
What is the CVE assigned to the WinRAR vulnerability exploited by the RomCom threat group in 2025?

- CVE-2025-8088 was assigned an 8.4 CVSS score in 2025 as per NIST. This is a high rating on the CVSS scale, the attack vector is local meaning that user interaction or manual execution is required in order for the exploit to work. In this scenario the user had opened a malicious winrar archive.

What is the nature of this vulnerability?

- This is a path traversal vulnerability, which allows attackers to execute arbitrary code by creating malicious archive files. The underlying method is the use of a COM 

What is the name of the archive file under Susan's documents folder that exploits the vulnerability upon opening the archive file?

- By using the MFTECmd utility from Eric Zimmerman I was able to locate files created that have the file extensions `.rar`. The tool itself will create a csv of all information stored in the Master File Table of a disk.
- The tool can be found at the internet archive and on Eric Zimmermans website, both links can be found in the references as well as a guide explaining how to use the MFTCmd utility. 
  `MFTECmd.exe -f E:\C\$Extend\$J -m E:\C\$MFT --csv "C:\RomCom" --csvf usnjrnl.csv`
- This created the `usnjrnl.csv` which contained every single change made to files on the system. After parsing the output for a file extension `.rar` I discovered the payload delivered by the phishing email.
- File Name: Pathology-Department-Research-Records.rar
- Created on the system: 2025-09-02 08:13:50.4403109

When was the archive file opened?
- This required finding the `.lnk` file that was used in the COM Hijack. By exploring the timeline after the `.rar` file was created i discovered a `.lnk` file was created shortly after the file was changed. This file was named `Pathology-Department-Research-Records.lnk`. (Note LNK files are created by the windows system to point to resources)
- The file archive was opened on: 2025-09-02 08:14:04.9964274

What is the name of the decoy document extracted from the archive file, meant to appear legitimate and distract the user?
- The file that was created to misdirect the user was named `Genotyping_Results_B57_Positive.pdf` it was discovered by filtering out all files that resided in the user `susan`'s home directory.

What is the name and path of the actual backdoor executable dropped by the archive file?
- The file created directly after the zip archive was opened was `C:\Users\susan\AppData\Local\ApbxHelper.exe` This is an odd location for an exe, usually the reside on the users desktop or within an area that is designated for programs but almost never in the AppData location. 

The exploit also drops a file to facilitate the persistence and execution of the backdoor. What is the path and name of this file?
- The first bat file to be executed on the system was `CollectSyncLogs.bat` This was executed from the OneDrive directory, another not normal place for a bat file to be executed for expected system administration operations. This is a persistence mechanism because if the device is connected to a OneDrive then the script may survive a clean wipe, if it is not connected to OneDrive then this is a place where no one would routinely look for scripts.
- Note that there was also a ps1 file that was executed however this was related to the admin using the KAPE tool which is used for system forensics.
- For the purposes of system level persistence though one file stuck out in the user `susan`'s startup directory: `C:\Users\susan\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Display Settings.lnk`
- This is the answer to the question because this file was writeable by the user and is executed every time the user logs on.

What is the associated MITRE Technique ID discussed in the previous question?
- This is associated with the MITRE Technique ID: T1547.009
- The definition is: ```
```
Adversaries may create or modify shortcuts that can execute a program during system boot or user login. Shortcuts or symbolic links are used to reference other files or programs that will be opened or executed when the shortcut is clicked or executed by a system startup process.
```

When was the decoy document opened by the end user, thinking it to be a legitimate document?
- After pulling up all changes made to the decoy PDF the next set of timestamps was a file update, which reflects the time a file was last accessed.
- The timestamp was: 2025-09-02 08:15:05


## Tools and References
[Ars Technica, Dan Goodin, Aug 2025](https://arstechnica.com/security/2025/08/high-severity-winrar-0-day-exploited-for-weeks-by-2-groups/)

[Mythic C2 Documentation]( http://docs.mythic-c2.net/home)

[MFTECmd Reference](https://www.cyberengage.org/post/ntfs-journaling-in-digital-forensics-logfile-usnjrnl-parsing-of-j-logfile-using-mftecmd-ex)

[SANS MFTECmd.exe backlink](https://web.archive.org/web/20240329180255if_/https://f001.backblazeb2.com/file/EricZimmermanTools/MFTECmd.zip)

[Eric Zimmerman's Forensic Toolkit:](https://ericzimmerman.github.io/#!index.md)

[NIST CVE Score for WinRar Vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2025-8088)

[MITRE Technique for startup persistence:]( https://attack.mitre.org/techniques/T1547/009/)
