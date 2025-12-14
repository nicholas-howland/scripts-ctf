import string

# recursively creates every possible key
def generate_strings(current_string, length):
    possibleChars=string.ascii_letters + string.digits;
    if len(current_string) == length:
        print(current_string)
        return
    for pos in range(62):
        generate_strings(current_string + possibleChars[pos], length)
# generate_strings("", 5)


def bruteForceKey(current_string, length,knownLastChar=""):
    possibleChars=string.ascii_letters + string.digits;
    if len(current_string) == length:
#        print(current_string)
        possible_keys.append(current_string)
        return 
    for pos in range(62):
        bruteForceKey(current_string + possibleChars[pos], length)

def getKeyChar(knownChar,encodedChar):
    character= bytes.fromhex(encodedChar)
    return chr(ord(knownChar) ^ ord(character))

def tryKey(key,encodedFlag,knownLastChar):
    byte_string = bytes.fromhex(encodedFlag)
    flag = byte_string.decode('utf-8')
    xored = ""
    for i in range(0,len(flag)):
        xored += chr(ord(flag[i]) ^ ord(key[i%len(key)]))
    if(xored[-1]==knownLastChar):
        print(key)
        print(xored)


# get the first chunk of the key
knownFirstChunk="THM{"
discoveredKey=""
encodedFlag='6005082937052c293c3371353113334079263924752337612658013c3a1246393c623246350a203a'
partialPass=""
for i in range(4):
    partialPass=partialPass+getKeyChar(knownFirstChunk[i],encodedFlag[i*2]+encodedFlag[(i*2)+1])


print("first part of password is: "+partialPass)
possible_keys=[]
bruteForceKey(partialPass,5)

for i in possible_keys:
    tryKey(i,encodedFlag,"}")


















