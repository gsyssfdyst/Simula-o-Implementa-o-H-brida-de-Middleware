Markdown

# Simulação Avançada de Sistema Distribuído Híbrido

Este projeto é uma simulação acadêmica de um sistema distribuído complexo, projetado para explorar conceitos avançados de comunicação, liderança, tolerância a falhas e segurança em ambientes distribuídos. A arquitetura implementa um modelo híbrido, onde dois grupos de nós operam com diferentes tecnologias de middleware e algoritmos de eleição, coordenados para funcionar como um sistema coeso.

## Conceitos e Tecnologias Implementadas

- **Middleware Híbrido**:
    - [cite_start]**Grupo A**: Utiliza **gRPC** para comunicação de alta performance baseada em RPCs. [cite: 38]
    - [cite_start]**Grupo B**: Utiliza **Pyro5** para uma abordagem flexível de RMI (Remote Method Invocation). [cite: 39]
- **Algoritmos de Eleição de Líder**:
    - [cite_start]**Grupo A**: Implementa o algoritmo **Bully**, onde nós com IDs mais altos se impõem como líderes. [cite: 59]
    - [cite_start]**Grupo B**: Implementa o algoritmo em **Anel**, onde uma mensagem de eleição circula entre os nós para determinar o novo líder. [cite: 60]
- **Sincronização Temporal**:
    - [cite_start]Todos os eventos e mensagens no sistema são marcados com o tempo lógico utilizando **Relógios de Lamport**, garantindo uma ordenação causal parcial dos eventos. [cite: 35]
- **Detecção de Falhas e Tolerância**:
    - [cite_start]Um mecanismo de **Heartbeat** é usado para monitorar a atividade dos líderes. [cite: 66]
    - [cite_start]O sistema reage automaticamente a falhas, acionando um novo processo de eleição após 3 falhas de heartbeat consecutivas. [cite: 67, 68]
- **Segurança e Autenticação**:
    - [cite_start]A comunicação é protegida por um sistema de **autenticação baseado em token JWT**, com tempo de expiração para validar as sessões. [cite: 73, 74]
- **Comunicação Multigrupo**:
    - [cite_start]**Intra-grupo**: A comunicação dentro de cada grupo é gerenciada pelas respectivas tecnologias de middleware (gRPC e Pyro5). [cite: 33]
    - [cite_start]**Inter-grupo**: A infraestrutura para comunicação entre os grupos via **UDP Multicast** está implementada em `common/multicast.py`. [cite: 34]

## Estrutura dos Diretórios

O projeto está organizado de forma modular para separar as responsabilidades de cada componente:

.
├── common/             # Módulos compartilhados (lógica de Lamport, autenticação, etc.)
│   ├── auth.py
│   └── lamport_clock.py
├── group_a/            # Implementação do Grupo A (gRPC e Bully)
│   ├── node_a.py
│   └── proto/
│       ├── group_comm.proto
│       ├── group_comm_pb2.py
│       └── group_comm_pb2_grpc.py
├── group_b/            # Implementação do Grupo B (Pyro5 e Anel)
│   └── node_b.py
├── config.py           # Arquivo de configuração central
├── requirements.txt    # Dependências do projeto
└── README.md           # Esta documentação


## Guia de Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior.
- As bibliotecas listadas no arquivo `requirements.txt`.

### Passos para Instalação

1.  **Clone o Repositório**:
    Faça o download de todos os arquivos mantendo a estrutura de diretórios acima.

2.  **Instale as Dependências**:
    Navegue até o diretório raiz do projeto e execute:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Compile os Protocol Buffers (gRPC)**:
    É necessário gerar o código Python a partir do arquivo `.proto`. Execute o seguinte comando no diretório raiz:
    ```bash
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. group_a/proto/group_comm.proto
    ```

### Executando a Simulação

Para executar a simulação, você precisará abrir múltiplos terminais. O sistema foi projetado para ter 3 nós em cada grupo.

**1. Inicie o Servidor de Nomes (Pyro5)**
Este passo é essencial para o Grupo B. Abra um terminal e execute:
```bash
pyro5-ns

Mantenha este processo em execução.

2. Inicie os Nós do Grupo A (gRPC)
Abra três terminais e execute um nó em cada um:
Bash

# Terminal 1
python group_a/node_a.py 1

# Terminal 2
python group_a/node_a.py 2

# Terminal 3
python group_a/node_a.py 3

3. Inicie os Nós do Grupo B (Pyro5)
Abra mais três terminais para os nós do Grupo B:
Bash

# Terminal 4
python group_b/node_b.py 4

# Terminal 5
python group_b/node_b.py 5

# Terminal 6
python group_b/node_b.py 6

Como Simular Falhas

Para testar a tolerância a falhas do sistema, você pode simular a queda de um líder.

    Identifique o terminal onde o nó líder de um dos grupos está sendo executado (inicialmente, será o nó de ID mais alto: 3 para o Grupo A e 6 para o Grupo B).

    Finalize o processo nesse terminal (usando Ctrl+C).

    Observe os outros terminais do mesmo grupo. Os nós subordinados detectarão a ausência de heartbeats e iniciarão automaticamente um novo processo de eleição para escolher um novo líder.