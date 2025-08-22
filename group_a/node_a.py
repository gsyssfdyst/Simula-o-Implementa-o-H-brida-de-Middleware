import grpc
import time
import sys
import threading
from concurrent import futures

# Adicionar caminhos para importações
sys.path.append('.')
sys.path.append('./group_a')

import config
from common.lamport_clock import LamportClock
from common.auth import AuthService
from proto import group_comm_pb2, group_comm_pb2_grpc

# Classe do Servidor gRPC para receber mensagens
class GroupACommsServicer(group_comm_pb2_grpc.GroupCommsServicer):
    def __init__(self, node_instance):
        self.node = node_instance

    def SendMessage(self, request, context):
        self.node.clock.update(request.lamport_time)
        print(f"[{self.node.node_id}] Mensagem recebida de {request.sender_id}: '{request.message}' | Relógio: {self.node.clock.get_time()}")
        return group_comm_pb2.MessageReply(response="ACK", lamport_time=self.node.clock.increment())

    def Election(self, request, context):
        # Lógica do Algoritmo Bully: Responde se tem um ID maior 
        if self.node.node_id > request.candidate_id:
            print(f"[{self.node.node_id}] Respondeu OK para eleição de {request.candidate_id}")
            # Idealmente, iniciaria sua própria eleição aqui se ainda não o fez.
            threading.Thread(target=self.node.start_election).start()
            return group_comm_pb2.ResponseMessage(success=True)
        return group_comm_pb2.ResponseMessage(success=False)

    def Victory(self, request, context):
        self.node.leader_id = request.leader_id
        print(f"[{self.node.node_id}] Novo líder do Grupo A é {self.node.leader_id}")
        return group_comm_pb2.ResponseMessage(success=True)
    
    def Heartbeat(self, request, context):
        return group_comm_pb2.HeartbeatResponse(alive=True)


class NodeA:
    def __init__(self, node_id):
        self.node_id = node_id
        self.node_info = config.GROUP_A_NODES[node_id]
        self.peers = {nid: info for nid, info in config.GROUP_A_NODES.items() if nid != node_id}
        self.leader_id = max(config.GROUP_A_NODES.keys()) # Começa assumindo o maior ID como líder
        self.is_election_happening = False

        self.clock = LamportClock()
        self.auth_service = AuthService()
        self.token = None
        
        # Heartbeat tracking [cite: 51]
        self.heartbeat_failures = {nid: 0 for nid in self.peers.keys()}

    def run(self):
        # Iniciar servidor gRPC em uma thread
        server_thread = threading.Thread(target=self.start_grpc_server)
        server_thread.daemon = True
        server_thread.start()
        print(f"[Nó {self.node_id}] Servidor gRPC iniciado na porta {self.node_info['middleware_port']}")

        # Aguardar um momento para os servidores subirem
        time.sleep(2)
        
        # Iniciar rotinas de heartbeat
        heartbeat_thread = threading.Thread(target=self.send_heartbeats)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

        # Simulação de interação
        self.simulate_client()

    def start_grpc_server(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        group_comm_pb2_grpc.add_GroupCommsServicer_to_server(GroupACommsServicer(self), server)
        server.add_insecure_port(f'[::]:{self.node_info["middleware_port"]}')
        server.start()
        server.wait_for_termination()

    def start_election(self):
        """Implementação do Algoritmo Bully """
        if self.is_election_happening:
            return
        
        self.is_election_happening = True
        print(f"[{self.node_id}] Iniciou uma eleição.")
        self.clock.increment()

        higher_nodes = [nid for nid in self.peers if nid > self.node_id]
        if not higher_nodes:
            # Se não há nós com ID maior, este nó vence.
            self.announce_victory()
            self.is_election_happening = False
            return

        responded = False
        for peer_id in higher_nodes:
            try:
                with grpc.insecure_channel(f'localhost:{self.peers[peer_id]["middleware_port"]}') as channel:
                    stub = group_comm_pb2_grpc.GroupCommsStub(channel)
                    response = stub.Election(group_comm_pb2.ElectionMessage(candidate_id=self.node_id), timeout=2)
                    if response.success:
                        print(f"[{self.node_id}] Eleição interrompida por {peer_id}.")
                        responded = True
                        break 
            except grpc.RpcError:
                print(f"[{self.node_id}] Nó {peer_id} não respondeu à eleição.")
        
        if not responded:
            self.announce_victory()

        self.is_election_happening = False

    def announce_victory(self):
        print(f"[{self.node_id}] Eu sou o novo líder!")
        self.leader_id = self.node_id
        for peer_id, peer_info in self.peers.items():
            try:
                with grpc.insecure_channel(f'localhost:{peer_info["middleware_port"]}') as channel:
                    stub = group_comm_pb2_grpc.GroupCommsStub(channel)
                    stub.Victory(group_comm_pb2.VictoryMessage(leader_id=self.node_id))
            except grpc.RpcError:
                print(f"[{self.node_id}] Falha ao anunciar vitória para {peer_id}.")

    def send_heartbeats(self):
        while True:
            time.sleep(config.HEARTBEAT_INTERVAL)
            if self.node_id == self.leader_id:
                continue # O líder não precisa checar ninguém (nesta implementação simplificada)
            
            try:
                leader_info = config.GROUP_A_NODES[self.leader_id]
                with grpc.insecure_channel(f'localhost:{leader_info["middleware_port"]}') as channel:
                    stub = group_comm_pb2_grpc.GroupCommsStub(channel)
                    stub.Heartbeat(group_comm_pb2.HeartbeatRequest(node_id=self.node_id), timeout=1)
                self.heartbeat_failures[self.leader_id] = 0 # Reset no sucesso
            except (grpc.RpcError, KeyError):
                self.heartbeat_failures[self.leader_id] += 1
                print(f"[{self.node_id}] Falha no heartbeat do líder {self.leader_id}. Tentativa {self.heartbeat_failures[self.leader_id]}")
                if self.heartbeat_failures[self.leader_id] >= config.MAX_FAILED_HEARTBEATS:
                    print(f"[{self.node_id}] Líder {self.leader_id} considerado inativo. Iniciando nova eleição. ")
                    self.start_election()
    
    def simulate_client(self):
        time.sleep(5)
        # Exemplo de envio de mensagem para o líder
        while True:
            if self.leader_id != self.node_id:
                try:
                    leader_info = config.GROUP_A_NODES[self.leader_id]
                    with grpc.insecure_channel(f'localhost:{leader_info["middleware_port"]}') as channel:
                        stub = group_comm_pb2_grpc.GroupCommsStub(channel)
                        msg_time = self.clock.increment()
                        response = stub.SendMessage(group_comm_pb2.MessageRequest(
                            sender_id=self.node_id,
                            message=f"Olá do nó {self.node_id}",
                            lamport_time=msg_time
                        ))
                        self.clock.update(response.lamport_time)
                        print(f"[{self.node_id}] Resposta do líder: '{response.response}' | Relógio: {self.clock.get_time()}")
                except (grpc.RpcError, KeyError):
                    print(f"[{self.node_id}] Não foi possível contatar o líder {self.leader_id}.")
            time.sleep(10)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python group_a/node_a.py <node_id>")
        sys.exit(1)
    
    node_id = int(sys.argv[1])
    if node_id not in config.GROUP_A_NODES:
        print(f"ID de nó inválido. IDs disponíveis para Grupo A: {list(config.GROUP_A_NODES.keys())}")
        sys.exit(1)
        
    node = NodeA(node_id)
    node.run()