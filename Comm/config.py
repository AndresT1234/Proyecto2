# Dirección y puerto del NameNode
NAME_NODE_HOST = "localhost"  # Host del NameNode
NAME_NODE_PORT = 5000         # Puerto del NameNode

# Lista de direcciones de los DataNodes (puedes agregar más)
DATA_NODE_HOSTS = [
    "localhost:50051",
    "localhost:50052",
    "localhost:50053"
]

# Tamaño de bloque para la fragmentación de archivos
BLOCK_SIZE = 1024 * 1024  # 1 MB

# Factor de replicación (cuántas copias de cada bloque se almacenarán)
REPLICATION_FACTOR = 3

