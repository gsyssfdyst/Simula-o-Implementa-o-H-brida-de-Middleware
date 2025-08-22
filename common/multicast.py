# common/multicast.py
import socket
import struct
import json

class MulticastCommunicator:
    def __init__(self, group_address, port):
        self.multicast_group = (group_address, port)

        # Criação do socket de envio
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock.settimeout(0.2)
        ttl = struct.pack('b', 1)
        self.send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        # Criação do socket de recebimento
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_sock.bind(('', port))
        group = socket.inet_aton(group_address)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def send(self, message_dict):
        try:
            message_bytes = json.dumps(message_dict).encode('utf-8')
            self.send_sock.sendto(message_bytes, self.multicast_group)
        except Exception as e:
            print(f"[Multicast] Erro ao enviar mensagem: {e}")

    def receive(self):
        try:
            data, address = self.recv_sock.recvfrom(1024)
            return json.loads(data.decode('utf-8')), address
        except socket.timeout:
            return None, None
        except Exception as e:
            print(f"[Multicast] Erro ao receber mensagem: {e}")
            return None, None