## Prompt
As a Threat Intelligence Analyst investigating Operation Dream Job, you have identified that the Lazarus Group utilized a variety of custom-built malware and tools to facilitate their operations. Your task is to analyze and gather intelligence on the malware utilized by this APT.

## Questions
According to MITRE ATT&CK, what previously known malware does DRATzarus share similarities with?
- According to the MITRE ATT&CK framework page for DRATzarus https://attack.mitre.org/software/S0694/, it shares similarities with Bankshot another Remote access tool used by the Lazarus group.

Which Windows API function does DRATzarus use to detect the presence of a debugger?
- On the same MITRE page it lists a number of API's that are used by DRATzarus including the `IsDebuggerPresent` API call.

Torisma is another piece of malware used by the Lazarus Group. According to MITRE, it has encrypted its C2 communications using XOR and which other method?
- The MITRE page for Torisma also lists VEST-32 as an encryption method used in addition to XOR. There is a link to a McAfee article from 2020 titled "Operation North Star: Behind The Scenes" which details how the malware interacts with the C2.
- Note that C2 Communications occur over HTTP or HTTPS as well

Which packing method has been used to obfuscate Torisma?
- LZ4 Compression was used as well as the payload being Base64 encoded and AES encrypted.

Analyze the provided ISO file and identify the executable contained within it?
- After unzipping the ISO file two files existed in the drive. One was a file named `InternalViewer.exe`

The executable found in the previous question was renamed. Can you identify its original name?
- By right clicking on the file the original file name was discovered to be `SumatraPDF.exe` This indicates that the malware has been reused or repurposed.

According to VirusTotal, when was the EXE from the previous question First Seen In The Wild?(UTC)
- By using the file hash of the `InternalViewer.exe` file `382bdd11c605882ccb149f0d23707a7ee5f4b89a` and looking it up on VirusTotal the first time it was seen in the wild was: `2020-08-13 08:44:50`

What packer was used to pack the executable from Question 6? (Full name)
- By using Detect it Easy I was able to find the packer that was used `Packer: UPX (3.96) [NRV,brute]` UPX stands for Ultimate Packer for Executables.

What is the full URL found within the macro in the document Salary_Lockheed_Martin_job_opportunities_confidential.doc?
- By using a simple find command I was able to discover a couple of URL's. The first url was `https://markettrendingcenter.com/lk_job_oppor.docx` and the second was a stylesheet `http://schemas.openxmlformats.org/drawingml/2006/main`
- The first one is odd because it seems to pull in a second document

Who is the author of the document and who last modified the document Salary_Lockheed_Martin_job_opportunities_confidential.doc?
- This was found by looking at the file properties

Analyze the "17.dotm" document. What is the directory where a suspicious folder was created? (Format: Give the path starting immediately after `<USER>`. Please pay attention to placeholder.)
- There are tools used to decompile vba macros including OleDump, however it takes a significant amount of time to set up if I remember correctly. By dropping the docm file into virus total a list of files that were accessed by the vba script. The path `\AppData\Local\Microsoft\Notice` stood out to me because it does not seem to exist on normal sysetms.

Which suspicious file was checked for existence in that directory?
- There were a number of files that were accessed in that directory all of which are as follows
```
wsuser.db
wsuser.db.123.Manifest
wsuser.db.124.Manifest
wsuser.db.Manifest
```



DRATzarus: https://attack.mitre.org/software/S0694/
Bankshot: https://attack.mitre.org/software/S0239/
Torisma: https://attack.mitre.org/software/S0678/
Operation North Star: Behind The Scenes: https://www.mcafee.com/blogs/other-blogs/mcafee-labs/operation-north-star-behind-the-scenes/
Virus Total Page for InternalViewer.exe: https://www.virustotal.com/gui/file/adce894e3ce69c9822da57196707c7a15acee11319ccc963b84d83c23c3ea802/details
Tool Detect it Easy: https://github.com/horsicq/Detect-It-Easy



[[lazurus]] [[forensics]]
