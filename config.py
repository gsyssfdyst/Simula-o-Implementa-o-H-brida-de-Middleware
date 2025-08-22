MULTICAST_GROUP = '224.3.3.3'
MULTICAST_PORT = 5007


GROUP_A_NODES = {
    1: {'host': 'localhost', 'tcp_port': 8001, 'middleware_port': 80051},
    2: {'host': 'localhost', 'tcp_port': 8002, 'middleware_port': 80052},
    3: {'host': 'localhost', 'tcp_port': 8003, 'middleware_port': 80053},
}


GROUP_B_NODES = {
    4: {'host': 'localhost', 'tcp_port': 9004, 'middleware_port': 90091},
    5: {'host': 'localhost', 'tcp_port': 9005, 'middleware_port': 90092},
    6: {'host': 'localhost', 'tcp_port': 9006, 'middleware_port': 90093},
}


HEARTBEAT_INTERVAL = 7  
MAX_FAILED_HEARTBEATS = 3 


TOKEN_EXPIRATION_SECONDS = 360 
SECRET_KEY = "A!Very#Complex$Secret%Key^For*Auth_2025"

# Explicit ring topology mapping for Group B (used by the ring-election implementation)
RING_TOPOLOGY = {
    4: 5,
    5: 6,
    6: 4,
}