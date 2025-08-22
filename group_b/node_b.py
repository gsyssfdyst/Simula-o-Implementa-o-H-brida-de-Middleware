import Pyro5.api
import sys
import threading
import time
import socket

sys.path.append('.')
import config
from common.lamport_clock import LamportClock

@Pyro5.api.expose
class NodeB:
    def __init__(self, node_id):
        self.node_id = node_id
        self.node_info = config.GROUP_B_NODES[node_id]
        self.clock = LamportClock()
        self.leader_id = max(config.GROUP_B_NODES.keys()) # Assume o maior ID como líder inicial
        self.is_election_happening = False
        
        # Mapeamento do anel lógico 
        sorted_ids = sorted(config.GROUP_B_NODES.keys())
        my_index = sorted_ids.index(node_id)
        self.next_node_id = sorted_ids[(my_index + 1) % len(sorted_ids)]
        
        # Heartbeat
        self.heartbeat_failures = {nid: 0 for nid in config.GROUP_B_NODES}

    def message(self, sender_id, text, lamport_time):
        self.clock.update(lamport_time)
        print(f"[{self.node_id}] Mensagem de {sender_id}: '{text}' | Relógio: {self.clock.get_time()}")
        return f"ACK from {self.node_id}", self.clock.increment()

    def election(self, election_msg):
        """ Lógica do Algoritmo de Anel  """
        if self.node_id in election_msg['participants']:
            # A eleição deu a volta e chegou ao iniciador
            self.leader_id = max(election_msg['participants'])
            print(f"[{self.node_id}] Eleição finalizada. Novo líder: {self.leader_id}")
            self.is_election_happening = False
            # Anunciar o vencedor
            self.get_next_node_proxy().announce_victory(self.leader_id)
            return

        if not self.is_election_happening:
            self.is_election_happening = True
            election_msg['participants'].append(self.node_id)
            print(f"[{self.node_id}] Participando da eleição. Participantes: {election_msg['participants']}")
            self.get_next_node_proxy().election(election_msg)

    def announce_victory(self, leader_id):
        if self.leader_id == leader_id:
             # A mensagem de vitória deu a volta completa
            return
        print(f"[{self.node_id}] Anunciado novo líder do Grupo B: {leader_id}")
        self.leader_id = leader_id
        self.is_election_happening = False
        self.get_next_node_proxy().announce_victory(leader_id)

    def start_election(self):
        if self.is_election_happening:
            return
        
        print(f"[{self.node_id}] Iniciando eleição de anel...")
        self.is_election_happening = True
        self.get_next_node_proxy().election({'participants': [self.node_id]})

    def heartbeat(self):
        return True

    def get_next_node_proxy(self):
        uri = f"PYRONAME:node.b.{self.next_node_id}"
        return Pyro5.api.Proxy(uri)

def start_pyro_server(node):
    daemon = Pyro5.api.Daemon(host=node.node_info['host'])
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(node)
    ns.register(f"node.b.{node.node_id}", uri)
    print(f"[Nó {node.node_id}] Servidor Pyro5 pronto. Objeto registrado como node.b.{node.node_id}")
    daemon.requestLoop()

def send_heartbeats(node):
    time.sleep(5)
    while True:
        time.sleep(config.HEARTBEAT_INTERVAL)
        if node.node_id == node.leader_id or node.is_election_happening:
            continue
        
        try:
            uri = f"PYRONAME:node.b.{node.leader_id}"
            leader_proxy = Pyro5.api.Proxy(uri)
            leader_proxy.heartbeat()
            node.heartbeat_failures[node.leader_id] = 0
        except Exception:
            node.heartbeat_failures[node.leader_id] += 1
            print(f"[{node.node_id}] Falha no heartbeat do líder {node.leader_id}. Tentativa {node.heartbeat_failures[node.leader_id]}")
            if node.heartbeat_failures[node.leader_id] >= config.MAX_FAILED_HEARTBEATS:
                print(f"[{node.node_id}] Líder {node.leader_id} considerado inativo. Iniciando nova eleição. [cite: 53]")
                node.start_election()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python group_b/node_b.py <node_id>")
        sys.exit(1)

    node_id = int(sys.argv[1])
    if node_id not in config.GROUP_B_NODES:
        print(f"ID de nó inválido. IDs disponíveis para Grupo B: {list(config.GROUP_B_NODES.keys())}")
        sys.exit(1)
    
    node_b_instance = NodeB(node_id)
    
    server_thread = threading.Thread(target=start_pyro_server, args=(node_b_instance,))
    server_thread.daemon = True
    server_thread.start()

    heartbeat_thread = threading.Thread(target=send_heartbeats, args=(node_b_instance,))
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

    # Mantém a thread principal viva
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando nó.")