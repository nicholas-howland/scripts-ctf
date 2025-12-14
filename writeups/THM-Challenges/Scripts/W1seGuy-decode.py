import random
import socketserver 
import socket, os
import string


def tryKey(key):
    encodedFlag = "3a3c1b0b1f5f153a1e1b2b0c22311b1a40351b0c2f1a24430e02382f183a1c002f401a1c0c190212"
    byte_string = bytes.fromhex(encodedFlag)
    flag = byte_string.decode('utf-8')
    xored = ""
    for i in range(0,len(flag)):
        xored += chr(ord(flag[i]) ^ ord(key[i%len(key)]))
    print(xored)
    
    compareOutput(xored,key)

def compareOutput(xored,key):
    if(xored[0:4]=="THM{"):
        print(key)

# recursively creates every possible key
def generate_strings(current_string, length):
    possibleChars=string.ascii_letters + string.digits;
    if len(current_string) == length:
        print(current_string)
        return
    for pos in range(62):
        generate_strings(current_string + possibleChars[pos], length)
# generate_strings("", 5)


def bruteForceKey(current_string, length):
    possibleChars=string.ascii_letters + string.digits;
    if len(current_string) == length:
#        print(current_string)
        possible_keys.append(current_string)
        return 
    for pos in range(62):
        bruteForceKey(current_string + possibleChars[pos], length)

possible_keys=[]
compareOutput("THM","Sanity Check")
bruteForceKey("ntVpn",5)

for i in possible_keys:
    tryKey(i)


















