# Binary File Stuff

## bow.c
Mentioned in the NOTES.md as a referentail piece of code

## nop-sled.c
Example from GrayHatHacking that is used to demonstrate how binary files can be used to escallate privs on a machine

## buffer-overflow.py
This will test for buffer overflows on the program by entering a string of A's after a ":" is entered
Note pwntools is the library that is used here


# Pwntools Notes

Start a specific binary: `processObject = process(binary)`
Send a line of text after a character is recieved: `processObject.sendlineafter(b':', b'A'*numberOfChars)`
Recieve output and return the value to a string: `someString = processObject.recvall().decode()`
End the process forcefully, this is used to make sure the process ends before continuing onto the next command: `processObject.kill()`
Search throguh A binary to find a specific string location: `binary.search(b'/bin/sh\x00')`
