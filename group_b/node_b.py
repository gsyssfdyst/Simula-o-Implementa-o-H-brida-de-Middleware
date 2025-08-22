import Pyro5.api
import sys
import threading
import time
import socket

sys.path.append('.')
import config
from common.lamport_clock import LogicalClock

@Pyro5.api.expose
class PyroNode:
    """Um nó do Grupo B usando Pyro5 e eleição em anel.

    Responsabilidades:
    - Participar de eleições baseadas em anel.
    - Responder a RPCs (receive_data, election, announce_victory, heartbeat).
    - Manter um LogicalClock para timestamps de Lamport.
    """
    def __init__(self, node_id):
        self.node_id = node_id
        self.node_info = config.GROUP_B_NODES[node_id]
        self.clock = LogicalClock()
        self.leader_id = max(config.GROUP_B_NODES.keys())  # palpite inicial de líder
        self.is_election_happening = False

        # Usar topologia de anel explícita da configuração
        self.next_node_id = config.RING_TOPOLOGY.get(node_id, None)

        # Rastreamento de heartbeat para outros nós (indexado pelo id do nó)
        self.heartbeat_failures = {nid: 0 for nid in config.GROUP_B_NODES}

    def receive_data(self, sender_id, text, lamport_time):
        """Lidar com mensagens genéricas recebidas (renomeado de 'message')."""
        # sincronizar relógio lógico com timestamp recebido
        self.clock.sync(lamport_time)
        print(f"[{self.node_id}] receive_data de {sender_id}: '{text}' | relógio: {self.clock.get_current_time()}")
        # evento local: avançar o relógio para a resposta
        return f"ACK de {self.node_id}", self.clock.tick()

    def election(self, election_msg):
        """Lidar com mensagens de eleição em anel.

        formato de mensagem de eleição:
            {'participants': {node_id: lamport_timestamp, ...}}

        Quando a mensagem retorna a um participante existente, a eleição é concluída e
        o nó com o maior id se torna o líder.
        """
        participants = election_msg.get('participants', {})
        # Se já participamos, a eleição está concluída e devemos escolher o líder
        if self.node_id in participants:
            # Eleição concluída: escolher o maior ID como líder
            new_leader = max(participants.keys())
            self.leader_id = new_leader
            print(f"[{self.node_id}] Eleição finalizada. Novo líder: {self.leader_id}")
            self.is_election_happening = False
            # anunciar vencedor ao redor do anel
            self.get_next_node_proxy().announce_victory(self.leader_id)
            return

        # Caso contrário, participe e encaminhe com nosso timestamp
        if not self.is_election_happening:
            self.is_election_happening = True

        participants[self.node_id] = self.clock.get_current_time()
        print(f"[{self.node_id}] Participando da eleição. Participantes agora: {list(participants.keys())}")
        next_id = self.next_node_id
        print(f"[{self.node_id}] Encaminhando mensagem de eleição para o nó {next_id}")
        self.get_next_node_proxy().election({'participants': participants})

    def announce_victory(self, leader_id):
        """Receber e encaminhar o anúncio de vitória (semântica renomeada)."""
        if self.leader_id == leader_id:
            # Se a mensagem de vitória deu uma volta completa, pare de encaminhar
            return
        print(f"[{self.node_id}] Anunciado novo líder do Grupo B: {leader_id}")
        self.leader_id = leader_id
        self.is_election_happening = False
        # Encaminhar anúncio
        self.get_next_node_proxy().announce_victory(leader_id)

    def start_election(self):
        """Iniciar uma eleição em anel criando a estrutura de mensagem inicial."""
        if self.is_election_happening:
            return
        print(f"[{self.node_id}] Iniciando eleição em anel...")
        self.is_election_happening = True
        # usar um dicionário mapeando id -> timestamp ao entrar na eleição
        init_msg = {'participants': {self.node_id: self.clock.get_current_time()}}
        next_id = self.next_node_id
        print(f"[{self.node_id}] Enviando mensagem inicial de eleição para o nó {next_id}")
        self.get_next_node_proxy().election(init_msg)

    def heartbeat(self):
        """Resposta simples de heartbeat usada quando o líder chama este nó.

        Nós que não são líderes também usarão o loop send_heartbeats para verificar a vivacidade do líder.
        """
        # avançar no relógio na resposta de heartbeat é um evento local
        self.clock.tick()
        return True

    def get_next_node_proxy(self):
        uri = f"PYRONAME:node.b.{self.next_node_id}"
        return Pyro5.api.Proxy(uri)


def start_pyro_server(node):
    daemon = Pyro5.api.Daemon(host=node.node_info['host'])
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(node)
    ns.register(f"node.b.{node.node_id}", uri)
    print(f"[Nó {node.node_id}] Servidor Pyro5 pronto. Registrado como node.b.{node.node_id}")
    daemon.requestLoop()

def send_heartbeats(node):
    """Gerenciamento de loop de heartbeat.

    O líder ativa e pinge outros nós; os não-líderes tentam contatar o líder para detectar sua vivacidade.
    Isso inverte a lógica anterior, mas preserva a funcionalidade de detecção de falhas.
    """
    time.sleep(5)
    while True:
        time.sleep(config.HEARTBEAT_INTERVAL)
        if node.is_election_happening:
            continue

        # O líder ativa e pinga outros nós para verificar sua vivacidade
        if node.node_id == node.leader_id:
            for target_id in config.GROUP_B_NODES:
                if target_id == node.node_id:
                    continue
                try:
                    uri = f"PYRONAME:node.b.{target_id}"
                    proxy = Pyro5.api.Proxy(uri)
                    proxy.heartbeat()
                    node.heartbeat_failures[target_id] = 0
                except Exception:
                    node.heartbeat_failures[target_id] += 1
                    print(f"[{node.node_id}] Falha no heartbeat para o nó {target_id}. Tentativa {node.heartbeat_failures[target_id]}")
                    # Se um nó for considerado inativo, o líder pode registrar ou tomar outra ação
            continue

        # Os não-líderes ainda verificam a vivacidade do líder chamando o líder (detectando líder ausente)
        try:
            uri = f"PYRONAME:node.b.{node.leader_id}"
            leader_proxy = Pyro5.api.Proxy(uri)
            leader_proxy.heartbeat()
            # resposta recebida do líder, reiniciar contador
            node.heartbeat_failures[node.leader_id] = 0
        except Exception:
            node.heartbeat_failures[node.leader_id] += 1
            print(f"[{node.node_id}] Heartbeat perdido do líder {node.leader_id}. Tentativa {node.heartbeat_failures[node.leader_id]}")
            if node.heartbeat_failures[node.leader_id] >= config.MAX_FAILED_HEARTBEATS:
                print(f"[{node.node_id}] Líder {node.leader_id} considerado inativo. Iniciando nova eleição.")
                node.start_election()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python group_b/node_b.py <node_id>")
        sys.exit(1)

    node_id = int(sys.argv[1])
    if node_id not in config.GROUP_B_NODES:
        print(f"ID de nó inválido. IDs disponíveis para Grupo B: {list(config.GROUP_B_NODES.keys())}")
        sys.exit(1)

    node_b_instance = PyroNode(node_id)

    server_thread = threading.Thread(target=start_pyro_server, args=(node_b_instance,))
    server_thread.daemon = True
    server_thread.start()

    heartbeat_thread = threading.Thread(target=send_heartbeats, args=(node_b_instance,))
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

    # Manter a thread principal viva
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando nó.")