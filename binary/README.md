# Binary Exploitation repo

## Notes
Vulnerable functions include strcpy, gets, sprintf, scanf, strcat. 

## Programs
### Bow.c
Courtisy of Hack the Box, uses a single function to copy a string from a single function to a character buffer. Only works with address space layout randomization turned off. So effectively useless on in production/modern systems ( post 80s )



