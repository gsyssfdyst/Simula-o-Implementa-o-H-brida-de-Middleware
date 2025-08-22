# Simulação Avançada de Sistema Distribuído Híbrido

Este projeto é uma simulação acadêmica de um sistema distribuído híbrido (Grupo A = gRPC, Grupo B = Pyro5). Recentes mudanças no protocolo gRPC (arquivo group_a/proto/group_comm.proto) renomearam serviços e mensagens — veja instruções de recompilação abaixo.

Principais mudanças no .proto
- Serviço renomeado: GroupComms -> GroupAService
- Mensagem renomeada: VictoryMessage -> NewLeaderMessage
- Field novo em MessageRequest: client_version (string)
- Após alterar o .proto, é obrigatório regenerar os arquivos Python gerados pelo protoc.

Passos de preparação (obrigatório antes de executar qualquer nó do Grupo A)
1. Gere/regenere os arquivos Python a partir do .proto:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. group_a/proto/group_comm.proto
   ```
   Isso sobrescreverá:
   - group_a/proto/group_comm_pb2.py
   - group_a/proto/group_comm_pb2_grpc.py

2. Verifique que os arquivos gerados contêm:
   - service GroupAService {...}
   - message NewLeaderMessage { int32 leader_id = 1; }
   - message MessageRequest inclui client_version

3. Em seguida, inicie os nós do Grupo A (ex.: em terminais separados):
   ```bash
   python group_a/node_a.py 1
   python group_a/node_a.py 2
   python group_a/node_a.py 3
   ```
   Observação: node_a.py já foi atualizado para usar os novos nomes (GroupAService, NewLeaderMessage). Se você modificar o .proto novamente, repita o passo 1.

Execução completa (resumo)
1. Inicie o servidor de nomes Pyro5 (necessário para Grupo B):
   ```bash
   pyro5-ns
   ```
2. Inicie os nós do Grupo A (gRPC) — veja comandos acima.
3. Inicie os nós do Grupo B (Pyro5):
   ```bash
   python group_b/node_b.py 4
   python group_b/node_b.py 5
   python group_b/node_b.py 6
   ```

Notas rápidas
- O relógio lógico (Lamport) é usado para timestamps em todas as mensagens.
- Há mecanismo de heartbeat e eleição (Bully para Grupo A; Anel para Grupo B).
- Autenticação básica via JWT está disponível em common/auth.py; ajuste SECRET_KEY e TTL em config.py conforme necessário.

Se detectar erros de compatibilidade gRPC após regenerar os arquivos, atualize o pacote grpc/tools:
```bash
pip install --upgrade grpcio grpcio-tools
```

Mantenha o passo de recompilação como parte do seu fluxo de desenvolvimento sempre que editar `group_a/proto/group_comm.proto`.