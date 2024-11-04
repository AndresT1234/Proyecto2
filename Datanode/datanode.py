# datanode.py
import grpc
import os
from concurrent import futures
import sys

# Agrega la ruta de la carpeta proto a sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))

import dfs_pb2
import dfs_pb2_grpc


class DataNode(dfs_pb2_grpc.DataNodeServicer):
    def __init__(self, storage_path):
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    def StoreBlock(self, request, context):
        block_id = request.block_id
        data = request.data

        # Almacenar el bloque en un archivo
        file_path = os.path.join(self.storage_path, block_id)
        try:
            with open(file_path, "wb") as f:
                f.write(data)
            return dfs_pb2.StoreBlockResponse(success=True, message="Bloque almacenado exitosamente.")
        except Exception as e:
            return dfs_pb2.StoreBlockResponse(success=False, message=str(e))

    def RetrieveBlock(self, request, context):
        block_id = request.block_id
        file_path = os.path.join(self.storage_path, block_id)

        if not os.path.exists(file_path):
            return dfs_pb2.RetrieveBlockResponse(success=False, message="Bloque no encontrado.")

        try:
            with open(file_path, "rb") as f:
                data = f.read()
            return dfs_pb2.RetrieveBlockResponse(success=True, data=data, message="Bloque recuperado exitosamente.")
        except Exception as e:
            return dfs_pb2.RetrieveBlockResponse(success=False, message=str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dfs_pb2_grpc.add_DataNodeServicer_to_server(DataNode(storage_path='data_blocks'), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("DataNode escuchando en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
