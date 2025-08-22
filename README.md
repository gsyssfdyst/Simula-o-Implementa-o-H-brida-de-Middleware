# Simulação de Sistema Distribuído

Este projeto implementa uma simulação de sistema distribuído conforme especificado na atividade da disciplina de Sistemas Distribuídos. A simulação inclui dois grupos de processos com diferentes tecnologias de middleware, algoritmos de eleição, detecção de falhas e comunicação multigrupo.

## Estrutura do Projeto

```


├── group\_a/
│   ├── **init**.py
│   ├── node\_a.py
│   └── proto/
│       ├── **init**.py
│       ├── group\_comm.proto
│       └── group\_comm\_pb2\_grpc.py
│       └── group\_comm\_pb2.py
├── group\_b/
│   ├── **init**.py
│   ├── node\_b.py
├── common/
│   ├── **init**.py
│   ├── auth.py
│   ├── lamport\_clock.py
│   └── multicast.py
├── config.py
├── requirements.txt
└── README.md

````

## Pré-requisitos

- Python 3.8+
- Bibliotecas listadas em `requirements.txt`. [cite_start]A linguagem permitida é Python.

## Instalação

1.  Clone o repositório ou salve todos os arquivos na estrutura de diretórios descrita.
2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Compile os arquivos de protocolo do gRPC. No diretório raiz do projeto, execute:
    ```bash
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. group_a/proto/group_comm.proto
    ```

## Execução

A simulação requer a execução de múltiplos processos simultaneamente, cada um em seu próprio terminal. Para o Grupo B (Pyro5), é necessário iniciar o servidor de nomes primeiro.

### Passo 1: Iniciar o Servidor de Nomes do Pyro5

Abra um terminal e execute:

```bash
pyro5-ns
````

Mantenha este terminal aberto durante toda a simulação.

### Passo 2: Iniciar os Nós do Grupo A

O projeto exige 2 grupos de processos com 3 nós cada. Abra 3 terminais separados. Em cada um, execute um nó do Grupo A com seu respectivo ID:

```bash
# Terminal 1
python group_a/node_a.py 1

# Terminal 2
python group_a/node_a.py 2

# Terminal 3
python group_a/node_a.py 3
```

### Passo 3: Iniciar os Nós do Grupo B

Abra mais 3 terminais separados. Em cada um, execute um nó do Grupo B:

```bash
# Terminal 4
python group_b/node_b.py 4

# Terminal 5
python group_b/node_b.py 5

# Terminal 6
python group_b/node_b.py 6
```

### Observando a Simulação

  - **Eleição Inicial**: Os nós irão iniciar e, após um tempo, detectarão a "falha" do líder padrão e iniciarão um processo de eleição.
  - **Comunicação**: Os nós não-líderes enviarão mensagens periodicamente para seus respectivos líderes.
  - **Detecção de Falhas**: Para simular uma falha do líder, finalize o processo do nó líder (por exemplo, `Ctrl+C` no terminal do líder). Os outros nós do grupo detectarão a ausência de heartbeats e iniciarão uma nova eleição automaticamente, conforme o requisito.

## Componentes Implementados

  - **Comunicação Multigrupo**:
      - Comunicação intra-grupo: Implementada via Sockets TCP, utilizados implicitamente pelas bibliotecas gRPC e Pyro5.
      - Comunicação inter-grupo: A estrutura para UDP Multicast está pronta no módulo `common/multicast.py`.
  - **Middleware Híbrido**:
      - Grupo A: Comunicação baseada em gRPC.
      - Grupo B: Comunicação baseada em Pyro5 (alternativa a RMI).
  - **Sincronização**: Todos os processos usam relógios de Lamport para marcação de eventos.
  - **Liderança e Orquestração**:
      - Grupo A: Implementado o algoritmo de eleição de líder Bully.
      - Grupo B: Implementado o algoritmo de eleição de líder de Anel.
  - **Detecção de Falhas**:
      - Implementado um mecanismo de heartbeat entre os nós.
      - Após 3 falhas consecutivas, um nó é considerado inativo, e se for o líder, uma nova eleição é acionada.
  - **Políticas de Acesso**:
      - Desenvolvido um sistema de controle de acesso baseado em autenticação por token. O módulo `common/auth.py` implementa a geração e validação de tokens com tempo de expiração
  - **Código-Fonte Estruturado**: O projeto está modularizado e este README serve como documentação e instrução de execução.

<!-- end list -->

```
```