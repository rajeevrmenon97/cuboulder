import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('moxie',21234))

nums = []
data = sock.recv(1024)
data += sock.recv(1024)

for i in range(0, 14, 4):
   nums.append(struct.unpack('<I', data[i:i+4])[0])

sock.send(struct.pack('<Q', (sum(nums))))

print(sock.recv(1024))