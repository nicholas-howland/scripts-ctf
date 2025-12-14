# Writeup

## Objective
Pyrat receives a curious response from an HTTP server, which leads to a potential Python code execution vulnerability. With a cleverly crafted payload, it is possible to gain a shell on the machine. Delving into the directories, the author uncovers a well-known folder that provides a user with access to credentials. A subsequent exploration yields valuable insights into the application's older version. Exploring possible endpoints using a custom script, the user can discover a special endpoint and ingeniously expand their exploration by fuzzing passwords. The script unveils a password, ultimately granting access to the root.
## Target
10.10.186.173
## Steps Taken
- Based on the description I first started by taking a look at the well-known directory on the webserver port.
- Initial nmap scan:
```
PORT     STATE SERVICE
22/tcp   open  ssh
8000/tcp open  http-alt
```
- Strangely enough the machine did not have an http server port open however the 8000 port did allow for nc connections.
- When entering in commands that were not documented like `GET` the following was returned
`name 'GET' is not defined`
- When entering in commands that were documented but with invalid syntax the following was returned
`name 'ls' is not defined`
- This reminded me of some of the python syntax so I tried some python code and that seemed to work just fine. Next it was time to test importing libraries and printing stuff.
- After successfully getting a shell with the nc mkfifo reverse shell I was able to gain access to the system as www-data. I was not able to find the web root in known directories and tried looking in the systemd area.
- After poking around in the file directory I discovered a file in the /opt/dev/.git directory named config that had plaintext user credetnials for the think user that were as follows
```
username = think
password = _TH1NKINGPirate$_
```
- This revealed the first flag.
- The root flag is obtained by finding an old version of the python program running at `/root/pyrat.py`
- After gaining access to the users account I was able to use the `git list` and `git show` commands to look at recently pushed code which was as follows:
```
+...............................................
+
+def switch_case(client_socket, data):
+    if data == 'some_endpoint':
+        get_this_enpoint(client_socket)
+    else:
+        # Check socket is admin and downgrade if is not aprooved
+        uid = os.getuid()
+        if (uid == 0):
+            change_uid()
+
+        if data == 'shell':
+            shell(client_socket)
+        else:
+            exec_python(client_socket, data)
+
+def shell(client_socket):
+    try:
+        import pty
+        os.dup2(client_socket.fileno(), 0)
+        os.dup2(client_socket.fileno(), 1)
+        os.dup2(client_socket.fileno(), 2)
+        pty.spawn("/bin/sh")
+    except Exception as e:
+        send_data(client_socket, e
+
+...............................................
```
- Here we can see that some code was added to switch to a known endpoint aka socket. Using the function switch_case() function I was able to get the following output.
```
switch_case(client_socket, "something")
name 'something' is not defined
<socket.socket fd=9, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.10.186.173', 8000), raddr=('10.21.217.147', 39278)> : something
```
- I was able to dump the local environment variubles using the global() function call and printing it to stdout.
- No additional sockets were defined. I decided to define some and see if I could set the uid in the socket to be 0 using the following snippet `admin_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM);`
- My focus then shifted to attacking the switch_case function, the data was executed in the current socket somehow.
- After crashing the server (try hack me said they were forcing the server to reboot...) I decided to look up how the challenge was supposed to be completed...
- The challenge required touching "endpoints" as in one word variubles to expose inputs and outputs, not hacking the actual program itself. The writeup I learned from can be found here: https://medium.com/@stray0x1/pyrat-tryhackme-writeup-a51b8bb54823
- The code needed some tweaking to get working correctly but in essence what it does is query an "endpoint" named admin then brute forces a password field until the string "Welcome" is found in the output and then dumps the password value to the screen. This particular challenge uses the rockyou-75.txt wordlist in seclists. Once the correct password is used then a root shell is presented.

