"""
Reads container IDs from 'container.txt' and initiates an all to all ping.
THe output is stored in capture.json
"""

import re
import json
import time
import signal
import docker
import threading

client = docker.from_env()

_STOP = False
_PING_REGEX = '(\d+) bytes from ([\d\.]*): icmp_seq=(\d+) ttl=(\d+) time=([\d\.]+) ms'
_RESULT = []

def signal_handler(sig, frame):
    global _STOP
    print('Stopping pings')
    _STOP = True

def ping(container, ip):
    thread = threading.current_thread()
    self_ip = container.name.split('-')[-1]
    print("Pinging", ip, "from", self_ip)
    try:
        exec_log = container.exec_run("ping " + ip, stdout=True, stderr=True, stream=True)
        stats = {}
        stats['from'] = self_ip
        stats['to'] = ip
        stats['pings'] = []
        for line in exec_log[1]:
            if not getattr(thread, "do_run", True):
                break
            ping_data = {}
            ping_data['timestamp'] = int(time.time())
            result = re.search(_PING_REGEX, line.decode().rstrip())
            if result is not None:
                #ping_data['packet_size'] = result.groups()[0]
                #ping_data['icmp_seq'] = result.groups()[2]
                #ping_data['ttl'] = result.groups()[3]
                ping_data['latency'] = result.groups()[4]
                stats['pings'].append(ping_data)
        _RESULT.append(stats)
    except Exception as e:
        print("Could not ping", ip, "from", self_ip, container.name)

if __name__=="__main__":
    signal.signal(signal.SIGINT, signal_handler)

    containers = []
    container_ids = []
    ip_list = {}
    input_file = 'containers.txt'
    output_file = 'capture.json'

    with open(input_file) as file:
        for line in file:
            container_ids.append(line.rstrip())

    for id in container_ids:
        container = client.containers.get(id)
        containers.append(client.containers.get(id))
        ip_list[container.name] = container.name.split('-')[-1]

    threads = []

    for container in containers:
        self_ip = container.name.split('-')[-1]
        for ip in ip_list.values():
            if ip != self_ip:
                threads.append(threading.Thread(target=ping, args=(container, ip)))
                threads[-1].start()

    print("Press Ctrl^C to stop pinging")
    
    while not _STOP:
        continue
    print("Stopping threads")
    for thread in threads:
            thread.do_run = False
    for thread in threads:
            thread.join()

    with open(output_file, 'w') as fp:
        json.dump(_RESULT, fp, indent=4)

    print("Output written to", output_file)