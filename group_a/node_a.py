import sys
import time
import threading
from concurrent import futures

# Nota: Certifique-se de ter recompilado o .proto conforme instruído antes de executar este arquivo.

import grpc
sys.path.append('.')
import config
from common.lamport_clock import LogicalClock
from common.auth import TokenManager

# Import gerado pelo protoc (deve existir após recompilar)
from group_a.proto import group_comm_pb2 as pb2
from group_a.proto import group_comm_pb2_grpc as pb2_grpc


class GroupAServicer(pb2_grpc.GroupAServiceServicer):
    def __init__(self, node_id):
        self.node_id = node_id
        self.node_info = config.GROUP_A_NODES[node_id]
        self.clock = LogicalClock()
        self.leader_id = max(config.GROUP_A_NODES.keys())  # palpite inicial
        self.token_mgr = TokenManager()

    def SendMessage(self, request, context):
        # Sincroniza relógio com timestamp recebido e responde com novo tempo
        try:
            self.clock.sync(request.lamport_time)
        except Exception:
            pass
        local_time = self.clock.tick()
        print(f"[A{self.node_id}] ReceiveMessage from {request.sender_id}: '{request.message}' (lamport={request.lamport_time}) -> local={local_time}")
        return pb2.MessageReply(response=f"ACK from A{self.node_id}", lamport_time=local_time)

    def Election(self, request, context):
        # Implementação simples: se candidate_id maior que o nosso, aceitamos; respondemos sucesso sempre
        candidate = getattr(request, 'candidate_id', None)
        print(f"[A{self.node_id}] Election request received. Candidate: {candidate}")
        # Exemplo simplificado de lógica Bully: se o candidato tiver ID maior, atualizamos leader
        if candidate is not None and candidate > self.leader_id:
            self.leader_id = candidate
            print(f"[A{self.node_id}] Atualizando líder para {self.leader_id} (via Election)")
        return pb2.ResponseMessage(success=True)

    def NewLeader(self, request, context):
        # Nova mensagem renomeada de Victory -> NewLeaderMessage
        leader = getattr(request, 'leader_id', None)
        print(f"[A{self.node_id}] NewLeader announced: {leader}")
        if leader is not None:
            self.leader_id = leader
        return pb2.ResponseMessage(success=True)

    def Heartbeat(self, request, context):
        # Responde que está vivo; avança relógio local pois é um evento local
        self.clock.tick()
        return pb2.HeartbeatResponse(alive=True)


def serve(node_id):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = GroupAServicer(node_id)
    pb2_grpc.add_GroupAServiceServicer_to_server(servicer, server)
    port = servicer.node_info.get('middleware_port', 50051)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[A{node_id}] GroupA gRPC server started on port {port}. Leader guess: {servicer.leader_id}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
        print(f"[A{node_id}] Server stopped.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python group_a/node_a.py <node_id>")
        sys.exit(1)
    nid = int(sys.argv[1])
    if nid not in config.GROUP_A_NODES:
        print(f"ID inválido. IDs disponíveis para Grupo A: {list(config.GROUP_A_NODES.keys())}")
        sys.exit(1)
    serve(nid)