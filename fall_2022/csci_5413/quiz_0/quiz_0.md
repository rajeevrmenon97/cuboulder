# Quiz 0

1. Your laptop is connected to the internet via campus wireless. How would you find the IP address of the wireless interface of your laptop?

    **Answer:** The IP address for various interfaces can be found by running the following commands in the terminal/command prompt:

    Windows: `ipconfig`

    Mac: `ifconfig`

    Linux: `ifconfig` or `ip addr`

    The wireless interface name is usually `wlan0`, `wl0`, etc.

1. Your laptop is connected to the internet via campus wireless. You point your browser at whatismyip.com. What IP do you get? (Don’t just do this and give the number, tell me what host it belongs to.)

    **Answer:** This gives the public-facing IP address of the campus network after network address translation. It usually belongs to a server or router or any network device which is directly connected to the internet.

1. Your laptop is connected to the internet via campus wireless. You start a web server running on your laptop and call your mom, telling her to browse to the IP address you obtained in Problem 1. What happens?

    **Answer:** The IP address obtained in the first problem is the local IP address of the laptop in the local network. The subnet is hidden under multiple other networks using NAT. Hence that IP won't be accessible from outside the network.

1. Same as problem 3, but you tell mom to try the IP obtained in Problem 2. What happens now?

    **Answer:** The server won't be accessible using the public-facing IP obtained from problem 2 as well. For the server to be accessible, multiple port forwarding needs to be set up from the public-facing IP to the internal network to which the laptop is connected.

1. Using your CU account, you create a new webpage. When you try to access this page your browser says “403... Forbidden.” What’s likely the problem?

    **Answer:** The user is forbidden from accessing the particular web page. This might be due to the lack of permission to access the web page. The file permissions might need to be changed so that the web server user can access the web page file. The error can also occur when web pages are cached and/or are performing a forbidden action.

1. On a Linux system there are two files, f1 and f2. Both files contain the string **abcd** and nothing else. You edit f1 and change the **a** to a **b**. You then edit f2 and discover it contains **bbcd** just like file f1. Explain how this could happen.

    **Answer:** f1 and f2 are symbolic or hard linked. Symbolic links are shortcuts that refer to the file. Unlike symlinks, hard links refer to the inode of the file.

1. In x86 cores, we have a register called IP. What does it do (don’t just expand the acronym!)?

    **Answer:**: The Instruction Pointer is a register that holds the address of the next instruction to be executed in a program.

1. In x86 assembler, what two things does the `call` instruction do?
    
    **Answer:** The `call` instruction does two things:
    
    * It pushes the return address on the stack
    * Updates the instruction pointer to the call destination given along with the instruction.
    
    This transfers program control to the call target and begins execution from there.

1. There are several ways to forward a port on a Linux box; name any one method you know of. (You can name more than one if you want to show off, but I’m only going to score the first method you write.)

    **Answer:** A few ways to forward a port on a Linux machine are given below:
    * Port forwarding using iptables
    * Port forwarding using SSH tunnels
    * Using third-party tools like `socat`, `redir`, etc.

1. What does f() compute in the C program below?
    ```c
    int f(int a) {
        int i = 0;
        while (a) {
            a &= (a-1);
            i++;
        }
        return i;
    }
    ```

    **Answer:** The function calculates the number of set bits in the binary representation of the integer argument `a`.
