# Binary File Stuff

## bow.c
Mentioned in the NOTES.md as a referentail piece of code

## nop-sled.c
Example from GrayHatHacking that is used to demonstrate how binary files can be used to escallate privs on a machine

## buffer-overflow.py
This will test for buffer overflows on the program by entering a string of A's after a ":" is entered
Note pwntools is the library that is used here

# dump-hex-words.sh
This is a simple bash script that will print out all of the words that can be recreated in hexidecimal, fun for setting custom tags or cheeky responses as desired.

# Pwntools Notes

Start a specific binary: `processObject = process(binary)`
Send a line of text after a character is recieved: `processObject.sendlineafter(b':', b'A'*numberOfChars)`
Recieve output and return the value to a string: `someString = processObject.recvall().decode()`
End the process forcefully, this is used to make sure the process ends before continuing onto the next command: `processObject.kill()`
Search throguh A binary to find a specific string location: `binary.search(b'/bin/sh\x00')`


# pwndbg notes
pwndbg is a tool used for binary file inspection at runtime, it is super usefull when you need to debug a binary. It can be installed using the guide found here: https://pwndbg.re/stable/setup/. Note that some of the commands below will act differently before the binary is run versus after it is run.
`info functions` - prints out all the available functions, if the program has been run then it will try to pull in all of the functions from imported libraries
`rop` - This will print out all the rop gadgets in the binary that was called, if the program has been run in the past then it will try to print out all the rop gadgets in the included libraries as well
`set arg <string>` - This will set an argument to be called along with the binary, usefull for binaries that require command line arguments
`set arg $(cat payload)` - This will do exactly the same thing as the above except instead of using a static string whatever exists inside of the payload file will be supplied to the binary instead
`run` - This will run the binary with any arguments that were supplied
