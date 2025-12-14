# THM W1seGuy Writeup

## Prompt
Your friend told me you were wise, but I don't believe them. Can you prove me wrong?

When you are ready, click the Start Machine button to fire up the Virtual Machine. Please allow 3-5 minutes for the VM to start fully.

The server is listening on port 1337 via TCP. You can connect to it using Netcat or any other tool you prefer.

## Steps taken
- First I downloaded the script and reviewed the code. The key function is as follows: `''.join(random.choices(string.ascii_letters + string.digits, k=5))` after which it is hex encoded. The function used to encode the flag is as follows: *note the server argument can be ignored when running locally*
```
def setup(server, key):
    flag = 'THM{thisisafakeflag}' 
    xored = ""

    for i in range(0,len(flag)):
        xored += chr(ord(flag[i]) ^ ord(key[i%len(key)]))

    hex_encoded = xored.encode().hex()
    return hex_encoded
```
- This will produce a string of 5 upper and lower case alpha numeric digits that will serve as the key.
- The server will produce the XOR encoded flat upon connecting to the server thankfully so a script to brute force the key does not need to be made for the first flag
- Next to actually connect to the server and get the first encrypted key, once it is obtained we can take the encoded text and crack it offline to get the flag. The encoded flag is `3a3c1b0b1f5f153a1e1b2b0c22311b1a40351b0c2f1a24430e02382f183a1c002f401a1c0c190212`
- Now for the program design. First the program must accept the encoded flag -> xor the flag against the proposed key -> if the first four digets of the flag matches `THM{` then we found the first 4 chunks of the flag and the rest of the key can be guessed. This method is known as crib dragging.
- The first known character is xored against the decoded hexadecimal value of the first encoded value and the result is added to the known key. The known key is then used in conjunction with the known plaintext and the encoded value to decrypt the next chunk of the key. Once the first 4 characters are discovered the last key value can be brute forced by comparing the last character in the decoded text for each of the known values to the known character "}" that we know the flag format is in.
- The challenge server will end up using a script to crib drag for me using the xor encryption. This script can be found here: https://github.com/ExylumTechnical/scripts-ctf/blob/main/Cryptography/cribDragging-xor.py






