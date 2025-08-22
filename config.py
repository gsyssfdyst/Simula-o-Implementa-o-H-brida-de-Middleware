
MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007


GROUP_A_NODES = {
    1: {'host': 'localhost', 'tcp_port': 10001, 'middleware_port': 50051},
    2: {'host': 'localhost', 'tcp_port': 10002, 'middleware_port': 50052},
    3: {'host': 'localhost', 'tcp_port': 10003, 'middleware_port': 50053},
}


GROUP_B_NODES = {
    4: {'host': 'localhost', 'tcp_port': 20004, 'middleware_port': 9091},
    5: {'host': 'localhost', 'tcp_port': 20005, 'middleware_port': 9092},
    6: {'host': 'localhost', 'tcp_port': 20006, 'middleware_port': 9093},
}


HEARTBEAT_INTERVAL = 5  
MAX_FAILED_HEARTBEATS = 3 


TOKEN_EXPIRATION_SECONDS = 300 
SECRET_KEY = "uma-chave-secreta-muito-forte"