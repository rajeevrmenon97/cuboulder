# Homework 5 - Blade CTF challenges

## Level 1

We are presented with a blank HTML page with a form having username and password fields. Inspecting the source files using Chrome Dev tools we can see a Javascript file in the `cgi-bin` folder called `verify.js`. Opening the file we can see that the username and password are hard-coded in it.

## Level 2

We are presented with a page that lists all the active users on the server. On examining the Javascript for the website we see the following code:


```javascript
var f = document.getElementById("filter");
if (f != null) {
    if (f.value != '') {
    myurl = myurl + "?filter=" +  f.value;
    }
}
```

It looks for an element with the id `filter`. If it is found, it adds the element's value as a query parameter to the `users.php` script. We can use the Chrome Dev tools to inject an input field with the id `filter` and a button that calls the `getusers()` JS function on click.

```HTML
<input type="text" id="filter"/>
<button id="button" onclick="getusers()">GO</button>
```

On clicking the `GO` button, we can see that the output is now filtered according to the username provided in the textbox. Assuming the PHP script to be executing some sort of shell command in an insecure manner, we can try sending the `&` character URL-encoded to see if it does anything. On sending `%26 ls` as the input we get the output:

```
a
hi.txt
secretuser.txt
testblit
users.php
```

We can read the contents of the `secretuser.txt` file by sending `%26 cat secretuser.txt`.

## Level 3

In Level 3 we are presented with a form. On entering values in `First`, `Last`, `email` and `Comment` and clicking on the button, it submits the data to a Python script `/~level03/cgi-bin/petition.py` and we receive an ID for the comment. We can then use the ID field to retrieve the comment again. On examining the Python script in the server we see that the Python script creates a temporary file and writes some bytes into it. It then makes the file executable. In order to sanitize the inputs that we give in the field, the script then runs the temporary file with the data as argument. By writing the bytes to a file and using a decompiler like `ghidra` we see the following snippet:

```c
...
pcVar3 = strstr(local_414,"debug:");
...
sprintf(local_814,
        "echo %s | sed s/[]\\!\\\"#$%%\\&\\\'\\(\\)\\*+,\\/:\\;\\<=\\>?[\\\\\\^\\`{\\|}~]/\\ /g"
        ,pcVar3 + 6);
__stream_00 = popen(local_814,"r");
```

If a string of value `debug:` is present in the string, it then executes the command that follows it. On further examination of the program, we can see that it fails to sanitize, characters that are together. We can therefore get the `signers.txt` file by sending the following input: `debug::$$((cat signers.txt >> //tmp//signers.txt))`. Make sure that the file `/tmp/signers.txt` is writeable by anyone.

## Level 4

Level 4 presents us with a username and password field. Once we login, the username and password is stored in a PHP session. Then we are presented with another form, where we can specify a filename and some data. The data gets written to the file with the name specified. After that we are presented with a field where we can give our filename and read the contents of the file. 

Examining the default directory for PHP sessions (`/var/lib/php/sessions/`), we see multiple session files. Using path manipulation to read the session files, we can eventually get the required session using `../../../../var/lib/php/sessions/sess_91c7e1e10744d69fd8fe35ecfc`

## Level 5

Level 5 gives us a form with three fields `id`, `website`, and `password`. On inspecting the Python script, it opens a file with the same name as `id` and writes the website and password to it. There is an invisible form field called `admin` on the webpage. If it is set to `1`, the script displays the file with the same name as the value of the cookie called `user`. Using the Chrome Dev tools to set the cookie value of `user` to `zanardi` and setting the value of the `admin` field to `1`, we get the passwords saved by Zanardi.