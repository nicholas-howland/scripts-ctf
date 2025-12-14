# Writeup for The Future Is ******

## Cover challenge
It appeared that all the vials had a serial number of `544649434f4d49432e464f2f3f0d0a`

## Challenge 1. Gun

### Prompt
After gaining admin access to the smart rifle system, what is the flag?

### Solution
The sourcecode was provided for this challenge. The password hash was created by iterating through the encrypted password bytes, which were hexidecimal, and xoring them by the current positional value in the list. For example "abc" would
work like
char(a XOR 0)
char(b XOR 1)
char(c XOR 2)


## Challenge 2. nhm

### Prompt
Looks like one of our employees at the Hawaii Mass Driver Facility got tricked into handing over their personal information.

Can you take a look at this email and figure out what's going on?

### Solution
First I wanted to extract the attached document without opening the email or executing the code. I ended up manually copy and pasting the base64 encoded text that consisted of the source document and then decoded it with the base64 command like so:
`base64 --decode attachment.mime > PRIZE_ACCEPTANCE_FORM.docm`
The file type was confirmed as a document type `Microsoft Word 2007+` and the next step was to safely extract the macros without running the file.
"Windows files are just glorified zip files" after converting the .doc file to a zip archive I was able to see the list of files.
There was a vbaProject.bin file which after extracting the strings from the file the phrase "Send data to our C2 server" was seen as well as a google url `https://www.google.com/search?q=KEY{f8e504}` containing the flag for this challenge. 



















