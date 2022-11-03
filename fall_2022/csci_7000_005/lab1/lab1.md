# Advanced Network Systems - Lab Assignment 1

In cloudlab create experiment with profile: 3node-dataplane.

## 0. What are the IP Addresses of the nodes

- Node 0 - 192.168.1.1 - 90:e2:ba:ac:14:e8
- Node 1 - 192.168.1.2 - 90:e2:ba:b5:16:54
- Node 1 - 192.168.2.2 - 90:e2:ba:b5:16:55
- Node 2 - 192.168.2.1 - 90:e2:ba:b5:14:bc

## 1. Test Ping

### Check available interfaces

#### Node 0

```bash
node0:~> ifconfig
enp1s0f0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 128.105.145.77  netmask 255.255.252.0  broadcast 128.105.147.255
        inet6 fe80::72e4:22ff:fe83:c774  prefixlen 64  scopeid 0x20<link>
        ether 70:e4:22:83:c7:74  txqueuelen 1000  (Ethernet)
        RX packets 9561  bytes 642596 (642.5 KB)
        RX errors 0  dropped 0  overruns 1  frame 0
        TX packets 469  bytes 55354 (55.3 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device memory 0xc6a00000-c6afffff

enp6s0f0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.1  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::92e2:baff:feac:14e8  prefixlen 64  scopeid 0x20<link>
        ether 90:e2:ba:ac:14:e8  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 1125 (1.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 30  bytes 3625 (3.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 30  bytes 3625 (3.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

#### Node 1

```bash
node1:~> ifconfig
enp1s0f0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 128.105.145.78  netmask 255.255.252.0  broadcast 128.105.147.255
        inet6 fe80::72e4:22ff:fe84:1ac6  prefixlen 64  scopeid 0x20<link>
        ether 70:e4:22:84:1a:c6  txqueuelen 1000  (Ethernet)
        RX packets 15609  bytes 1009126 (1.0 MB)
        RX errors 0  dropped 0  overruns 2  frame 0
        TX packets 530  bytes 64245 (64.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device memory 0xc6a00000-c6afffff

enp6s0f0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.2  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::92e2:baff:feb5:1654  prefixlen 64  scopeid 0x20<link>
        ether 90:e2:ba:b5:16:54  txqueuelen 1000  (Ethernet)
        RX packets 2  bytes 685 (685.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 12  bytes 1285 (1.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enp6s0f1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.2.2  netmask 255.255.255.0  broadcast 192.168.2.255
        inet6 fe80::92e2:baff:feb5:1655  prefixlen 64  scopeid 0x20<link>
        ether 90:e2:ba:b5:16:55  txqueuelen 1000  (Ethernet)
        RX packets 1  bytes 362 (362.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 12  bytes 1285 (1.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 30  bytes 3625 (3.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 30  bytes 3625 (3.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

#### Node 2

```bash
node2:~> ifconfig
enp1s0f0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 128.105.145.158  netmask 255.255.252.0  broadcast 128.105.147.255
        inet6 fe80::72e4:22ff:fe84:6f2  prefixlen 64  scopeid 0x20<link>
        ether 70:e4:22:84:06:f2  txqueuelen 1000  (Ethernet)
        RX packets 9850  bytes 656849 (656.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 461  bytes 52781 (52.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device memory 0xc6a00000-c6afffff

enp6s0f0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.2.1  netmask 255.255.255.0  broadcast 192.168.2.255
        inet6 fe80::92e2:baff:feb5:14bc  prefixlen 64  scopeid 0x20<link>
        ether 90:e2:ba:b5:14:bc  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 9  bytes 1035 (1.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 30  bytes 3625 (3.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 30  bytes 3625 (3.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### Pinging Node 2 from Node 0

```bash
node0:~> ping -c5 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.
64 bytes from 192.168.2.1: icmp_seq=1 ttl=63 time=0.624 ms
64 bytes from 192.168.2.1: icmp_seq=2 ttl=63 time=0.307 ms
64 bytes from 192.168.2.1: icmp_seq=3 ttl=63 time=0.257 ms
64 bytes from 192.168.2.1: icmp_seq=4 ttl=63 time=0.289 ms
64 bytes from 192.168.2.1: icmp_seq=5 ttl=63 time=0.311 ms

--- 192.168.2.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4085ms
rtt min/avg/max/mdev = 0.257/0.357/0.624/0.134 ms
```

### Starting `tcpdump` on `enp6s0f0` in Node 1

```bash
node1:~> sudo tcpdump -i enp6s0f0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp6s0f0, link-type EN10MB (Ethernet), capture size 262144 bytes
17:55:43.646265 ARP, Request who-has node1-link-01 tell node0-link-01, length 46
17:55:43.646307 ARP, Reply node1-link-01 is-at 90:e2:ba:b5:16:54 (oui Unknown), length 28
17:55:43.646400 IP node0-link-01 > node2-link-12: ICMP echo request, id 1, seq 1, length 64
17:55:43.646725 IP node2-link-12 > node0-link-01: ICMP echo reply, id 1, seq 1, length 64
17:55:44.658749 IP node0-link-01 > node2-link-12: ICMP echo request, id 1, seq 2, length 64
17:55:44.658897 IP node2-link-12 > node0-link-01: ICMP echo reply, id 1, seq 2, length 64
17:55:45.682764 IP node0-link-01 > node2-link-12: ICMP echo request, id 1, seq 3, length 64
17:55:45.682905 IP node2-link-12 > node0-link-01: ICMP echo reply, id 1, seq 3, length 64
17:55:46.706759 IP node0-link-01 > node2-link-12: ICMP echo request, id 1, seq 4, length 64
17:55:46.706899 IP node2-link-12 > node0-link-01: ICMP echo reply, id 1, seq 4, length 64
17:55:47.730778 IP node0-link-01 > node2-link-12: ICMP echo request, id 1, seq 5, length 64
17:55:47.730924 IP node2-link-12 > node0-link-01: ICMP echo reply, id 1, seq 5, length 64
17:55:48.862617 ARP, Request who-has node0-link-01 tell node1-link-01, length 28
17:55:48.862744 ARP, Reply node0-link-01 is-at 90:e2:ba:ac:14:e8 (oui Unknown), length 46
14 packets captured
14 packets received by filter
0 packets dropped by kernel
```

## 2. eBPF Tutorial

Go through eBPF tutorial (at least basic01 and basic02, but you can do more).  You can use their virtual topology, or real interfaces, but eventually you'll need to use the real interfaces for the measurement in Step 4.
-- NOTE: The tutorial code was already downloaded to /tools/xdp-tutorial 


### 2.1 eBPF tutorial 1

https://github.com/xdp-project/xdp-tutorial/tree/master/basic01-xdp-pass

#### Loading `xdp_pass_user` on Node 1

```bash
node1:~> cd /tools/xdp-tutorial/basic01-xdp-pass/

node1:/tools/xdp-tutorial/basic01-xdp-pass> sudo ./xdp_pass_user -d enp6s0f0 --skb-mode
libbpf: Error loading BTF: Invalid argument(22)
libbpf: magic: 0xeb9f
version: 1
flags: 0x0
hdr_len: 24
type_off: 0
type_len: 256
str_off: 256
str_len: 223
btf_total_size: 503
[1] PTR (anon) type_id=2
[2] STRUCT xdp_md size=20 vlen=5
	data type_id=3 bits_offset=0
	data_end type_id=3 bits_offset=32
	data_meta type_id=3 bits_offset=64
	ingress_ifindex type_id=3 bits_offset=96
	rx_queue_index type_id=3 bits_offset=128
[3] TYPEDEF __u32 type_id=4
[4] INT unsigned int size=4 bits_offset=0 nr_bits=32 encoding=(none)
[5] FUNC_PROTO (anon) return=6 args=(1 ctx)
[6] INT int size=4 bits_offset=0 nr_bits=32 encoding=SIGNED
[7] FUNC xdp_prog_simple type_id=5 vlen != 0

libbpf: Error loading .BTF into kernel: -22.
Success: Loading XDP prog name:xdp_prog_simple(id:15) on device:enp6s0f0(ifindex:4)
```

#### Pinging Node 2 from Node 0 after loading `xdp_pass_user` on Node 1

```bash
node0:~> ping -c5 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.
64 bytes from 192.168.2.1: icmp_seq=1 ttl=63 time=0.265 ms
64 bytes from 192.168.2.1: icmp_seq=2 ttl=63 time=0.263 ms
64 bytes from 192.168.2.1: icmp_seq=3 ttl=63 time=0.247 ms
64 bytes from 192.168.2.1: icmp_seq=4 ttl=63 time=0.234 ms
64 bytes from 192.168.2.1: icmp_seq=5 ttl=63 time=0.233 ms

--- 192.168.2.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4086ms
rtt min/avg/max/mdev = 0.233/0.248/0.265/0.013 ms
```

#### Unloading the `xdp_pass_user` program

```bash
node1:/tools/xdp-tutorial/basic01-xdp-pass> sudo ./xdp_pass_user -d enp6s0f0 -U
```

### 2.2 eBPF Tutorial 2

https://github.com/xdp-project/xdp-tutorial/tree/master/basic02-prog-by-name

#### Load `xdp_drop`

```bash
node1:/tools/xdp-tutorial/basic01-xdp-pass> cd /tools/xdp-tutorial/basic02-prog-by-name/

node1:/tools/xdp-tutorial/basic02-prog-by-name> sudo ./xdp_loader --dev enp6s0f0 --force --progsec xdp_drop
libbpf: Error loading BTF: Invalid argument(22)
libbpf: magic: 0xeb9f
version: 1
flags: 0x0
hdr_len: 24
type_off: 0
type_len: 320
str_off: 320
str_len: 324
btf_total_size: 668
[1] PTR (anon) type_id=2
[2] STRUCT xdp_md size=20 vlen=5
	data type_id=3 bits_offset=0
	data_end type_id=3 bits_offset=32
	data_meta type_id=3 bits_offset=64
	ingress_ifindex type_id=3 bits_offset=96
	rx_queue_index type_id=3 bits_offset=128
[3] TYPEDEF __u32 type_id=4
[4] INT unsigned int size=4 bits_offset=0 nr_bits=32 encoding=(none)
[5] FUNC_PROTO (anon) return=6 args=(1 ctx)
[6] INT int size=4 bits_offset=0 nr_bits=32 encoding=SIGNED
[7] FUNC xdp_pass_func type_id=5 vlen != 0

libbpf: Error loading .BTF into kernel: -22.
BPF object (xdp_prog_kern) listing avail --progsec names
 xdp_pass
 xdp_drop
 xdp_abort
Success: Loaded BPF-object(xdp_prog_kern.o) and used section(xdp_drop)
 - XDP prog attached on device:enp6s0f0(ifindex:4)
```

#### Pinging Node 2 from Node 0 after loading `xdp_drop` on Node 1

```bash
node0:~> ping -c5 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.

--- 192.168.2.1 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4087ms
```

#### Load `xdp_pass`

```bash
node1:/tools/xdp-tutorial/basic02-prog-by-name> sudo ./xdp_loader --dev enp6s0f0 --force --progsec xdp_pass
libbpf: Error loading BTF: Invalid argument(22)
libbpf: magic: 0xeb9f
version: 1
flags: 0x0
hdr_len: 24
type_off: 0
type_len: 320
str_off: 320
str_len: 324
btf_total_size: 668
[1] PTR (anon) type_id=2
[2] STRUCT xdp_md size=20 vlen=5
	data type_id=3 bits_offset=0
	data_end type_id=3 bits_offset=32
	data_meta type_id=3 bits_offset=64
	ingress_ifindex type_id=3 bits_offset=96
	rx_queue_index type_id=3 bits_offset=128
[3] TYPEDEF __u32 type_id=4
[4] INT unsigned int size=4 bits_offset=0 nr_bits=32 encoding=(none)
[5] FUNC_PROTO (anon) return=6 args=(1 ctx)
[6] INT int size=4 bits_offset=0 nr_bits=32 encoding=SIGNED
[7] FUNC xdp_pass_func type_id=5 vlen != 0

libbpf: Error loading .BTF into kernel: -22.
BPF object (xdp_prog_kern) listing avail --progsec names
 xdp_pass
 xdp_drop
 xdp_abort
Success: Loaded BPF-object(xdp_prog_kern.o) and used section(xdp_pass)
 - XDP prog attached on device:enp6s0f0(ifindex:4)
```

#### Pinging Node 2 from Node 0 after loading `xdp_pass` on Node 1

```bash
node0:~> ping -c5 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.
64 bytes from 192.168.2.1: icmp_seq=1 ttl=63 time=0.372 ms
64 bytes from 192.168.2.1: icmp_seq=2 ttl=63 time=0.225 ms
64 bytes from 192.168.2.1: icmp_seq=3 ttl=63 time=0.253 ms
64 bytes from 192.168.2.1: icmp_seq=4 ttl=63 time=0.235 ms
64 bytes from 192.168.2.1: icmp_seq=5 ttl=63 time=0.219 ms

--- 192.168.2.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4093ms
rtt min/avg/max/mdev = 0.219/0.260/0.372/0.056 ms
```

#### Load `xdp_abort`

```bash
node1:/tools/xdp-tutorial/basic02-prog-by-name> sudo ./xdp_loader --dev enp6s0f0 --force --progsec xdp_abort
libbpf: Error loading BTF: Invalid argument(22)
libbpf: magic: 0xeb9f
version: 1
flags: 0x0
hdr_len: 24
type_off: 0
type_len: 320
str_off: 320
str_len: 324
btf_total_size: 668
[1] PTR (anon) type_id=2
[2] STRUCT xdp_md size=20 vlen=5
	data type_id=3 bits_offset=0
	data_end type_id=3 bits_offset=32
	data_meta type_id=3 bits_offset=64
	ingress_ifindex type_id=3 bits_offset=96
	rx_queue_index type_id=3 bits_offset=128
[3] TYPEDEF __u32 type_id=4
[4] INT unsigned int size=4 bits_offset=0 nr_bits=32 encoding=(none)
[5] FUNC_PROTO (anon) return=6 args=(1 ctx)
[6] INT int size=4 bits_offset=0 nr_bits=32 encoding=SIGNED
[7] FUNC xdp_pass_func type_id=5 vlen != 0

libbpf: Error loading .BTF into kernel: -22.
BPF object (xdp_prog_kern) listing avail --progsec names
 xdp_pass
 xdp_drop
 xdp_abort
Success: Loaded BPF-object(xdp_prog_kern.o) and used section(xdp_abort)
 - XDP prog attached on device:enp6s0f0(ifindex:4)
```

#### Pinging Node 2 from Node 0 after loading `xdp_abort` on Node 1

```bash
node0:~> ping -c5 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.

--- 192.168.2.1 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4097ms
```

#### Recording `xdp_exception` tracepoint with `perf`

```bash
node1:/tools/xdp-tutorial/basic02-prog-by-name> sudo perf record -a -e xdp:xdp_exception sleep 4
[ perf record: Woken up 1 times to write data ]
[ perf record: Captured and wrote 0.171 MB perf.data (3 samples) ]
```

#### Read `perf.data` and display the trace records

```bash
node1:/tools/xdp-tutorial/basic02-prog-by-name> sudo perf script
         swapper     0 [009]   887.703401: xdp:xdp_exception: prog_id=45 action=ABORTED ifindex=4
         swapper     0 [009]   888.727382: xdp:xdp_exception: prog_id=45 action=ABORTED ifindex=4
         swapper     0 [009]   889.751355: xdp:xdp_exception: prog_id=45 action=ABORTED ifindex=4
```

#### Unload the XDP program

```bash
node1:/tools/xdp-tutorial/basic02-prog-by-name> sudo ./xdp_loader --dev enp6s0f0 -U
INFO: xdp_link_detach() removed XDP prog ID:45 on ifindex:4
```

## 3. Load the eBPF IP router on node 1's interfaces.  Note: the tutorial uses the virtual environment (network name spaces)

### Check if any programs are loaded on Node 1

```bash
node1~> sudo bpftool net list
xdp:

tc:

flow_dissector:

```

### Check if Node 2 can be pinged from Node 0

```bash
node0:~> ping -c5 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.
64 bytes from 192.168.2.1: icmp_seq=1 ttl=63 time=0.355 ms
64 bytes from 192.168.2.1: icmp_seq=2 ttl=63 time=0.200 ms
64 bytes from 192.168.2.1: icmp_seq=3 ttl=63 time=0.253 ms
64 bytes from 192.168.2.1: icmp_seq=4 ttl=63 time=0.246 ms
64 bytes from 192.168.2.1: icmp_seq=5 ttl=63 time=0.237 ms

--- 192.168.2.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4104ms
rtt min/avg/max/mdev = 0.200/0.258/0.355/0.051 ms
```

### Build the program on Node 1

```bash
node1:/tools/xdp-tutorial/basic02-prog-by-name> cd /tools/xdp-tutorial/packet03-redirecting

node1:/tools/xdp-tutorial/packet03-redirecting> mv xdp_prog_kern.c xdp_prog_kern.c.bak

node1:/tools/xdp-tutorial/packet03-redirecting> cp ../packet-solutions/xdp_prog_kern_03.c ./xdp_prog_kern.c

node1:/tools/xdp-tutorial/packet03-redirecting> make clean
rm -rf ../libbpf/src//build
make -C ../libbpf/src/ clean
make[1]: Entering directory '/tools/xdp-tutorial/libbpf/src'
rm -rf *.o *.a *.so *.so.* *.pc ./sharedobjs ./staticobjs
make[1]: Leaving directory '/tools/xdp-tutorial/libbpf/src'
make -C ../common clean
make[1]: Entering directory '/tools/xdp-tutorial/common'
rm -f *.o
make[1]: Leaving directory '/tools/xdp-tutorial/common'
rm -f xdp_prog_user xdp_prog_kern.o xdp_prog_user.o xdp_loader xdp_stats
rm -f *.ll
rm -f *~

node1:/tools/xdp-tutorial/packet03-redirecting> make
make[1]: Entering directory '/tools/xdp-tutorial/libbpf/src'
mkdir -p ./staticobjs
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c bpf.c -o staticobjs/bpf.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c btf.c -o staticobjs/btf.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c libbpf.c -o staticobjs/libbpf.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c libbpf_errno.c -o staticobjs/libbpf_errno.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c netlink.c -o staticobjs/netlink.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c nlattr.c -o staticobjs/nlattr.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c str_error.c -o staticobjs/str_error.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c libbpf_probes.c -o staticobjs/libbpf_probes.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c bpf_prog_linfo.c -o staticobjs/bpf_prog_linfo.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c xsk.c -o staticobjs/xsk.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c btf_dump.c -o staticobjs/btf_dump.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64   -c hashmap.c -o staticobjs/hashmap.o
ar rcs libbpf.a staticobjs/bpf.o staticobjs/btf.o staticobjs/libbpf.o staticobjs/libbpf_errno.o staticobjs/netlink.o staticobjs/nlattr.o staticobjs/str_error.o staticobjs/libbpf_probes.o staticobjs/bpf_prog_linfo.o staticobjs/xsk.o staticobjs/btf_dump.o staticobjs/hashmap.o
mkdir -p ./sharedobjs
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c bpf.c -o sharedobjs/bpf.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c btf.c -o sharedobjs/btf.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c libbpf.c -o sharedobjs/libbpf.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c libbpf_errno.c -o sharedobjs/libbpf_errno.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c netlink.c -o sharedobjs/netlink.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c nlattr.c -o sharedobjs/nlattr.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c str_error.c -o sharedobjs/str_error.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c libbpf_probes.c -o sharedobjs/libbpf_probes.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c bpf_prog_linfo.c -o sharedobjs/bpf_prog_linfo.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c xsk.c -o sharedobjs/xsk.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c btf_dump.c -o sharedobjs/btf_dump.o
cc -I. -I../include -I../include/uapi -g -O2 -Werror -Wall -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -fPIC -fvisibility=hidden -DSHARED  -c hashmap.c -o sharedobjs/hashmap.o
cc -shared -Wl,--version-script=libbpf.map \
	      -Wl,-soname,libbpf.so.0 \
	      sharedobjs/bpf.o sharedobjs/btf.o sharedobjs/libbpf.o sharedobjs/libbpf_errno.o sharedobjs/netlink.o sharedobjs/nlattr.o sharedobjs/str_error.o sharedobjs/libbpf_probes.o sharedobjs/bpf_prog_linfo.o sharedobjs/xsk.o sharedobjs/btf_dump.o sharedobjs/hashmap.o  -lelf -o libbpf.so.0.0.6
ln -sf libbpf.so.0.0.6 libbpf.so.0
ln -sf libbpf.so.0 libbpf.so
sed -e "s|@PREFIX@|/usr|" \
	-e "s|@LIBDIR@|/usr/lib64|" \
	-e "s|@VERSION@|0.0.6|" \
	< libbpf.pc.template > libbpf.pc
make[1]: Leaving directory '/tools/xdp-tutorial/libbpf/src'
make[1]: Entering directory '/tools/xdp-tutorial/libbpf/src'
if [ ! -d 'build/usr/include/bpf' ]; then install -d -m 755 'build/usr/include/bpf'; fi; install bpf.h libbpf.h btf.h xsk.h libbpf_util.h bpf_helpers.h bpf_helper_defs.h bpf_tracing.h bpf_endian.h bpf_core_read.h -m 644 'build/usr/include/bpf'
make[1]: Leaving directory '/tools/xdp-tutorial/libbpf/src'
make -C ../common
make[1]: Entering directory '/tools/xdp-tutorial/common'
gcc -g -Wall -I../libbpf/src//build/usr/include/  -I../headers -c -o common_params.o common_params.c
gcc -g -Wall -I../libbpf/src//build/usr/include/  -I../headers -c -o common_user_bpf_xdp.o common_user_bpf_xdp.c
gcc -g -Wall -I../libbpf/src//build/usr/include/  -I../headers -c -o common_libbpf.o common_libbpf.c
make[1]: Leaving directory '/tools/xdp-tutorial/common'
cc -Wall -I../libbpf/src//build/usr/include/ -g -I../headers/ -L../libbpf/src/ -o xdp_prog_user ../common/common_params.o ../common/common_user_bpf_xdp.o \
 xdp_prog_user.c -l:libbpf.a -lelf
clang -S \
    -target bpf \
    -D __BPF_TRACING__ \
    -I../libbpf/src//build/usr/include/ -I../headers/ \
    -Wall \
    -Wno-unused-value \
    -Wno-pointer-sign \
    -Wno-compare-distinct-pointer-types \
    -Werror \
    -O2 -emit-llvm -c -g -o xdp_prog_kern.ll xdp_prog_kern.c
llc -march=bpf -filetype=obj -o xdp_prog_kern.o xdp_prog_kern.ll
make -C ../common/../basic-solutions xdp_loader
make[1]: Entering directory '/tools/xdp-tutorial/basic-solutions'
cc -Wall -I../libbpf/src//build/usr/include/ -g -I../headers/ -L../libbpf/src/ -o xdp_loader ../common//common_libbpf.o ../common//common_params.o ../common//common_user_bpf_xdp.o \
 xdp_loader.c -l:libbpf.a -lelf
make[1]: Leaving directory '/tools/xdp-tutorial/basic-solutions'
cp ../common/../basic-solutions/xdp_loader xdp_loader
make -C ../common/../basic-solutions xdp_stats
make[1]: Entering directory '/tools/xdp-tutorial/basic-solutions'
cc -Wall -I../libbpf/src//build/usr/include/ -g -I../headers/ -L../libbpf/src/ -o xdp_stats ../common//common_libbpf.o ../common//common_params.o ../common//common_user_bpf_xdp.o \
 xdp_stats.c -l:libbpf.a -lelf
make[1]: Leaving directory '/tools/xdp-tutorial/basic-solutions'
cp ../common/../basic-solutions/xdp_stats xdp_stats
```

### Load the program on both interfaces of Node 1

```bash
node1:/tools/xdp-tutorial/packet03-redirecting> sudo ./xdp_loader --dev enp6s0f0 --force --progsec xdp_router
libbpf: Error loading BTF: Invalid argument(22)
libbpf: magic: 0xeb9f
version: 1
flags: 0x0
hdr_len: 24
type_off: 0
type_len: 552
str_off: 552
str_len: 3891
btf_total_size: 4467
[1] PTR (anon) type_id=2
[2] STRUCT xdp_md size=20 vlen=5
	data type_id=3 bits_offset=0
	data_end type_id=3 bits_offset=32
	data_meta type_id=3 bits_offset=64
	ingress_ifindex type_id=3 bits_offset=96
	rx_queue_index type_id=3 bits_offset=128
[3] TYPEDEF __u32 type_id=4
[4] INT unsigned int size=4 bits_offset=0 nr_bits=32 encoding=(none)
[5] FUNC_PROTO (anon) return=6 args=(1 ctx)
[6] INT int size=4 bits_offset=0 nr_bits=32 encoding=SIGNED
[7] FUNC xdp_icmp_echo_func type_id=5 vlen != 0

libbpf: Error loading .BTF into kernel: -22.
Success: Loaded BPF-object(xdp_prog_kern.o) and used section(xdp_router)
 - XDP prog attached on device:enp6s0f0(ifindex:4)
 - Pinning maps in /sys/fs/bpf/enp6s0f0/

node1:/tools/xdp-tutorial/packet03-redirecting> sudo ./xdp_loader --dev enp6s0f1 --force --progsec xdp_router
libbpf: Error loading BTF: Invalid argument(22)
libbpf: magic: 0xeb9f
version: 1
flags: 0x0
hdr_len: 24
type_off: 0
type_len: 552
str_off: 552
str_len: 3891
btf_total_size: 4467
[1] PTR (anon) type_id=2
[2] STRUCT xdp_md size=20 vlen=5
	data type_id=3 bits_offset=0
	data_end type_id=3 bits_offset=32
	data_meta type_id=3 bits_offset=64
	ingress_ifindex type_id=3 bits_offset=96
	rx_queue_index type_id=3 bits_offset=128
[3] TYPEDEF __u32 type_id=4
[4] INT unsigned int size=4 bits_offset=0 nr_bits=32 encoding=(none)
[5] FUNC_PROTO (anon) return=6 args=(1 ctx)
[6] INT int size=4 bits_offset=0 nr_bits=32 encoding=SIGNED
[7] FUNC xdp_icmp_echo_func type_id=5 vlen != 0

libbpf: Error loading .BTF into kernel: -22.
Success: Loaded BPF-object(xdp_prog_kern.o) and used section(xdp_router)
 - XDP prog attached on device:enp6s0f1(ifindex:5)
 - Pinning maps in /sys/fs/bpf/enp6s0f1/
```

### Verify if the programs are loaded on Node 1

```bash
node1:/tools/xdp-tutorial/packet03-redirecting> sudo bpftool net list
xdp:
enp6s0f0(4) driver id 52
enp6s0f1(5) driver id 60

tc:

flow_dissector:

```

### Ping Node 2 from Node 0

```bash
node0:~> ping -c5 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.
64 bytes from 192.168.2.1: icmp_seq=1 ttl=63 time=0.210 ms
64 bytes from 192.168.2.1: icmp_seq=2 ttl=63 time=0.183 ms
64 bytes from 192.168.2.1: icmp_seq=3 ttl=63 time=0.222 ms
64 bytes from 192.168.2.1: icmp_seq=4 ttl=63 time=0.211 ms
64 bytes from 192.168.2.1: icmp_seq=5 ttl=63 time=0.222 ms

--- 192.168.2.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4074ms
rtt min/avg/max/mdev = 0.183/0.209/0.222/0.014 ms
```

### Collect stats from first interface `enp6s0f0`

```bash
node1:/tools/xdp-tutorial/packet03-redirecting> sudo ./xdp_stats -d enp6s0f0

Collecting stats from BPF map
 - BPF map (bpf_map_type:6) id:9 name:xdp_stats_map key_size:4 value_size:16 max_entries:5
XDP-action
XDP_ABORTED            0 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250290
XDP_DROP               0 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250278
XDP_PASS               2 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250276
XDP_TX                 0 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250276
XDP_REDIRECT           1 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250272
```

### Collect stats from second interface `enp6s0f1`

```bash
node1:/tools/xdp-tutorial/packet03-redirecting> sudo ./xdp_stats -d enp6s0f1

Collecting stats from BPF map
 - BPF map (bpf_map_type:6) id:13 name:xdp_stats_map key_size:4 value_size:16 max_entries:5
XDP-action
XDP_ABORTED            0 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250255
XDP_DROP               0 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250255
XDP_PASS               3 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250253
XDP_TX                 0 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250251
XDP_REDIRECT           6 pkts (         0 pps)           0 Kbytes (     0 Mbits/s) period:0.250251
```

### Unload the program from both the interfaces

```bash
node1:/tools/xdp-tutorial/packet03-redirecting> sudo ./xdp_loader --dev enp6s0f0 -U
INFO: xdp_link_detach() removed XDP prog ID:52 on ifindex:4

node1:/tools/xdp-tutorial/packet03-redirecting> sudo ./xdp_loader --dev enp6s0f1 -U
INFO: xdp_link_detach() removed XDP prog ID:60 on ifindex:5
```

## 4. Measure performance of eBPF Router and Linux router

Suggest starting with node1 with no eBPF programs loaded.  Verify you can ping from node0 to node2 still.

### Check if any programs are loaded on Node 1

```bash
node1:~> sudo bpftool net list
xdp:

tc:

flow_dissector:

```

### Check if Node 2 can be pinged from Node 0

```bash
node0:~> ping -c5 192.168.2.1
PING 192.168.2.1 (192.168.2.1) 56(84) bytes of data.
64 bytes from 192.168.2.1: icmp_seq=1 ttl=63 time=0.481 ms
64 bytes from 192.168.2.1: icmp_seq=2 ttl=63 time=0.248 ms
64 bytes from 192.168.2.1: icmp_seq=3 ttl=63 time=0.250 ms
64 bytes from 192.168.2.1: icmp_seq=4 ttl=63 time=0.240 ms
64 bytes from 192.168.2.1: icmp_seq=5 ttl=63 time=0.239 ms

--- 192.168.2.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4079ms
rtt min/avg/max/mdev = 0.239/0.291/0.481/0.094 ms
```

### 4.1 Setup DPDK on Node 0

#### Set up huge pages

```bash
node0:~> cd /tools/dpdk-stable-21.11.1/usertools/

node0:/tools/dpdk-stable-21.11.1/usertools> sudo ./dpdk-hugepages.py -p 1G --setup 2G
```

#### Bring down the interface to Node 0 in Node 1 `enp6s0f0` and unbind the kernel driver

```bash
node0:/tools/dpdk-stable-21.11.1/usertools> sudo ifconfig enp6s0f0 down

node0:/tools/dpdk-stable-21.11.1/usertools> lspci | grep Eth
01:00.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
01:00.1 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
06:00.0 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
06:00.1 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)

node1:/tools/dpdk-stable-21.11.2/usertools> sudo ./dpdk-devbind.py -u 06:00.0
```

#### Load userspace drivers as kernel modules in Node 0

```bash
node0:/tools/dpdk-stable-21.11.1/usertools> cd /tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio

node0:/tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio> sudo modprobe uio

node0:/tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio> sudo insmod igb_uio.ko
```

#### Verify if the modules are loaded in Node 0

```bash
node0:/tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio> lsmod | grep uio
igb_uio                20480  0
uio                    20480  1 igb_uio
```

#### Bind the device with the userspace driver in Node 0

```bash
node0:/tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio> cd /tools/dpdk-stable-21.11.1/usertools/

node0:/tools/dpdk-stable-21.11.1/usertools> sudo ./dpdk-devbind.py -b igb_uio 06:00.0
```

#### Start pktgen on Node 0

```bash
node0:/tools/dpdk-stable-21.11.1/usertools> cd /tools/Pktgen-DPDK

node0:/tools/Pktgen-DPDK> sudo ./start_pktgen.sh
```

##### Set source MAC and IP to Node 0's MAC and IP 

```bash
Pktgen:/> set 0 src mac 90:e2:ba:ac:14:e8

Pktgen:/> set 0 src ip 192.168.1.1
src IP address should contain subnet value, default /32 for IPv4
```

##### Set destination MAC to Node 1's MAC and destination IP to Node 2's IP

```bash
Pktgen:/> set 0 dst mac 90:e2:ba:b5:16:54

Pktgen:/> set 0 dst ip 192.168.2.1
```

##### Set rate and start Pktgen

```bash
Pktgen:/> set 0 rate 1

Pktgen:/> start 0
```

##### Stop pktgen

```bash
Pktgen:/> stop 0
```

#### Starting `tcpdump` on `enp6s0f0` in Node 1

```bash
node1:~> sudo tcpdump -i enp6s0f0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp6s0f0, link-type EN10MB (Ethernet), capture size 262144 bytes
17:55:43.646265 ARP, Request who-has node1-link-01 tell node0-link-01, length 46
17:55:43.646307 ARP, Reply node1-link-01 is-at 90:e2:ba:b5:16:54 (oui Unknown), length 28
18:23:40.470722 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.470722 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.470739 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.470739 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.470756 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.471062 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.471062 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.471062 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.471062 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.471062 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.471062 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:40.471062 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6

14613 packets captured
57424 packets received by filter
42687 packets dropped by kernel
```

#### Starting `tcpdump` on `enp6s0f0` in Node 2

```bash
node1:~> sudo tcpdump -i enp6s0f0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp6s0f0, link-type EN10MB (Ethernet), capture size 262144 bytes
17:55:43.646265 ARP, Request who-has node2-link-01 tell node1-link-02, length 46
17:55:43.646307 ARP, Reply node2-link-01 is-at 90:e2:ba:b5:14:bc (oui Unknown), length 28
18:23:58.138564 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:58.138564 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:58.138565 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:58.138565 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:58.138565 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:58.138565 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:58.138565 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:23:58.138571 IP node2-link-12.5678 > node0-link-01.1234: Flags [R], seq 305419920, win 0, length 0
18:23:58.138572 IP node2-link-12.5678 > node0-link-01.1234: Flags [R], seq 305419920, win 0, length 0
18:23:58.138574 IP node2-link-12.5678 > node0-link-01.1234: Flags [R], seq 305419920, win 0, length 0
18:23:58.138575 IP node2-link-12.5678 > node0-link-01.1234: Flags [R], seq 305419920, win 0, length 0
18:23:58.138577 IP node2-link-12.5678 > node0-link-01.1234: Flags [R], seq 305419920, win 0, length 0
18:23:58.138578 IP node2-link-12.5678 > node0-link-01.1234: Flags [R], seq 305419920, win 0, length 0
18:23:58.138580 IP node2-link-12.5678 > node0-link-01.1234: Flags [R], seq 305419920, win 0, length 0

131154 packets captured
434544 packets received by filter
303218 packets dropped by kernel
```

### 4.2 Repeat setup on node 2 

#### Setup huge pages, bind device with userspace drivers on Node 2

```bash
node2:~> cd /tools/dpdk-stable-21.11.1/usertools/

node2:/tools/dpdk-stable-21.11.1/usertools> sudo ./dpdk-hugepages.py -p 1G --setup 2G

node2:/tools/dpdk-stable-21.11.1/usertools> sudo ifconfig enp6s0f0 down

node2:/tools/dpdk-stable-21.11.1/usertools> lspci | grep Eth
01:00.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
01:00.1 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
06:00.0 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
06:00.1 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)

node2:/tools/dpdk-stable-21.11.1/usertools> sudo ./dpdk-devbind.py -u 06:00.0

node2:/tools/dpdk-stable-21.11.1/usertools> cd /tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio

node2:/tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio> sudo modprobe uio

node2:/tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio> sudo insmod igb_uio.ko

node2:/tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio> lsmod | grep uio
igb_uio                20480  0
uio                    20480  1 igb_uio

node2:/tools/dpdk-kmods-e68a705cc5dc3d1333bbcd722fe4e9a6ba3ee648/linux/igb_uio> cd /tools/dpdk-stable-21.11.1/usertools/

node2:/tools/dpdk-stable-21.11.1/usertools> sudo ./dpdk-devbind.py -b igb_uio 06:00.0
```

#### Start Pktgen on Node 2

```bash
node2:/tools/dpdk-stable-21.11.1/usertools> cd /tools/Pktgen-DPDK/

node2:/tools/Pktgen-DPDK> sudo ./start_pktgen.sh
```

#### Start sending traffic from Pktgen on Node 0

```bash
Pktgen:/> start 0
```

#### Run `tcpdump` on `enp6s0f0` in Node 1

```bash
node1:~> sudo tcpdump -i enp6s0f0 > o.txt
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp6s0f0, link-type EN10MB (Ethernet), capture size 262144 bytes
18:44:50.418738 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 305419896:305419902, ack 305419920, win 8192, length 6
18:44:50.418738 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:44:50.418739 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:44:50.418739 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:44:50.418739 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:44:50.418739 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:44:50.418739 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:44:50.418739 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:44:50.418768 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:44:50.418768 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
786217 packets captured
788069 packets received by filter
27 packets dropped by kernel
```

#### Run `tcpdump` on `enp6s0f1` in Node 1

```bash
node1:~> sudo tcpdump -i enp6s0f1
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp6s0f1, link-type EN10MB (Ethernet), capture size 262144 bytes
18:47:21.854624 ARP, Request who-has node2-link-12 tell node1-link-12, length 28
18:47:22.878621 ARP, Request who-has node2-link-12 tell node1-link-12, length 28
18:47:23.902644 ARP, Request who-has node2-link-12 tell node1-link-12, length 28
18:47:24.926614 ARP, Request who-has node2-link-12 tell node1-link-12, length 28
18:47:25.950668 ARP, Request who-has node2-link-12 tell node1-link-12, length 28

5 packets captured
5 packets received by filter
0 packets dropped by kernel
```

### 4.3 Set ARP table on node 1 (for the IP and MAC address of node 2) 

#### Setting up ARP table entry for Node 2 on Node 1

```bash
node1:~> sudo arp -s 192.168.2.1 90:e2:ba:b5:14:bc
```

#### Run `tcpdump` on `enp6s0f1` in Node 1

```bash
node1:~> sudo tcpdump -i enp6s0f1 > o.txt
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp6s0f1, link-type EN10MB (Ethernet), capture size 262144 bytes
18:49:43.330977 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 305419896:305419902, ack 305419920, win 8192, length 6
18:49:43.330981 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:49:43.330982 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:49:43.330984 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:49:43.330985 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:49:43.330986 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:49:43.330987 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6
18:49:43.330988 IP node0-link-01.1234 > node2-link-12.5678: Flags [.], seq 0:6, ack 1, win 8192, length 6

281012 packets captured
282431 packets received by filter
0 packets dropped by kernel
```

### 4.4 Measuring performance for Linux router

| Command           | Pkts/s Tx on Node 1   | Pkts/s Rx on Node 2   |
| ----------------- | --------------------- | --------------------- |
| set 0 rate 0.001  | 192                   | 192                   |
| set 0 rate 0.01   | 1536                  | 1536                  |
| set 0 rate 0.1    | 14920                 | 14920                 |
| set 0 rate 1      | 148866                | 148864                |
| set 0 rate 2      | 297664                | 297664                |
| set 0 rate 5      | 744315                | 744215                |
| set 0 rate 6      | 893140                | 893137                |
| set 0 rate 7      | 1041866               | 1041845               |
| set 0 rate 8      | 1190858               | 1190813               |
| set 0 rate 8.5    | 1265301               | 1265312               |
| set 0 rate 8.75   | 1302189               | 1292377               |
| set 0 rate 9      | 1339940               | 1297732               |
| set 0 rate 10     | 1488524               | 1297732               |
| set 0 rate 20     | 2977038               | 1297732               |
| set 0 rate 30     | 4465561               | 1297739               |
| set 0 rate 40     | 5923414               | 1297744               |

### Load eBPF router on Node 1

```bash
node1:~> cd /tools/xdp-tutorial/packet03-redirecting
node1:/tools/xdp-tutorial/packet03-redirecting> sudo ./xdp_loader --dev enp6s0f0 --force --progsec xdp_router
libbpf: Error loading BTF: Invalid argument(22)
libbpf: magic: 0xeb9f
version: 1
flags: 0x0
hdr_len: 24
type_off: 0
type_len: 552
str_off: 552
str_len: 3891
btf_total_size: 4467
[1] PTR (anon) type_id=2
[2] STRUCT xdp_md size=20 vlen=5
	data type_id=3 bits_offset=0
	data_end type_id=3 bits_offset=32
	data_meta type_id=3 bits_offset=64
	ingress_ifindex type_id=3 bits_offset=96
	rx_queue_index type_id=3 bits_offset=128
[3] TYPEDEF __u32 type_id=4
[4] INT unsigned int size=4 bits_offset=0 nr_bits=32 encoding=(none)
[5] FUNC_PROTO (anon) return=6 args=(1 ctx)
[6] INT int size=4 bits_offset=0 nr_bits=32 encoding=SIGNED
[7] FUNC xdp_icmp_echo_func type_id=5 vlen != 0

libbpf: Error loading .BTF into kernel: -22.
Success: Loaded BPF-object(xdp_prog_kern.o) and used section(xdp_router)
 - XDP prog attached on device:enp6s0f0(ifindex:4)
 - Unpinning (remove) prev maps in /sys/fs/bpf/enp6s0f0/
 - Pinning maps in /sys/fs/bpf/enp6s0f0/

node1:/tools/xdp-tutorial/packet03-redirecting> sudo ./xdp_loader --dev enp6s0f1 --force --progsec xdp_router
libbpf: Error loading BTF: Invalid argument(22)
libbpf: magic: 0xeb9f
version: 1
flags: 0x0
hdr_len: 24
type_off: 0
type_len: 552
str_off: 552
str_len: 3891
btf_total_size: 4467
[1] PTR (anon) type_id=2
[2] STRUCT xdp_md size=20 vlen=5
	data type_id=3 bits_offset=0
	data_end type_id=3 bits_offset=32
	data_meta type_id=3 bits_offset=64
	ingress_ifindex type_id=3 bits_offset=96
	rx_queue_index type_id=3 bits_offset=128
[3] TYPEDEF __u32 type_id=4
[4] INT unsigned int size=4 bits_offset=0 nr_bits=32 encoding=(none)
[5] FUNC_PROTO (anon) return=6 args=(1 ctx)
[6] INT int size=4 bits_offset=0 nr_bits=32 encoding=SIGNED
[7] FUNC xdp_icmp_echo_func type_id=5 vlen != 0

libbpf: Error loading .BTF into kernel: -22.
Success: Loaded BPF-object(xdp_prog_kern.o) and used section(xdp_router)
 - XDP prog attached on device:enp6s0f1(ifindex:5)
 - Unpinning (remove) prev maps in /sys/fs/bpf/enp6s0f1/
 - Pinning maps in /sys/fs/bpf/enp6s0f1/
node1:/tools/xdp-tutorial/packet03-redirecting>
```

### 4.5 Measuring performance for eBPF router

| Command           | Pkts/s Tx on Node 1   | Pkts/s Rx on Node 2   |
| ----------------- | --------------------- | --------------------- |
| set 0 rate 0.001  | 192                   | 192                   |                      
| set 0 rate 0.01   | 1536                  | 1536                  |
| set 0 rate 0.1    | 14916                 | 14912                 |
| set 0 rate 1      | 148867                | 148866                |
| set 0 rate 5      | 744289                | 744282                |
| set 0 rate 10     | 1488539               | 1488537               |
| set 0 rate 20     | 2977072               | 2977064               |
| set 0 rate 25     | 3721325               | 3721295               |
| set 0 rate 27     | 4021872               | 4021774               |
| set 0 rate 28     | 4170743               | 4170543               |
| set 0 rate 29     | 4316743               | 4183274               |
| set 0 rate 30     | 4465561               | 4188410               |
| set 0 rate 40     | 5954114               | 4188410               |
