import grpc
import requests
from autenticador import AuthManager
import os
import sys
from configuracioncliente import Config

# Agrega la ruta de la carpeta proto a sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))

import dfs_pb2
import dfs_pb2_grpc

class FileManager:
    def __init__(self):
        self.current_directory = "/"
        self.auth_manager = AuthManager()

    def authenticate(self, username, password):
        return self.auth_manager.authenticate(username, password)

    def put_file(self, filename):
        try:
            with open(filename, "rb") as f:
                file_data = f.read()
        except FileNotFoundError:
            print(f"Archivo: {filename} no se encontró.")
            return
        except Exception as e:
            print(f"Error leyendo el archivo {filename}. {e}")
            return
        
        # Dividir archivo en bloques
        blocks = [file_data[i:i + 1024] for i in range(0, len(file_data), 1024)]
        block_ids = []
        
        # Almacenar cada bloque en el DataNode
        for i, block in enumerate(blocks):
            block_id = f"{os.path.basename(filename)}_block_{i}"
            block_ids.append(block_id)
            
            with grpc.insecure_channel(Config.DATANODE_URL) as channel:
                stub = dfs_pb2_grpc.DataNodeStub(channel)
                response = stub.StoreBlock(dfs_pb2.StoreBlockRequest(block_id=block_id, data=block))
                if not response.success:
                    print(f"Error almacenando el bloque {block_id}")
        
        # Registrar los metadatos en el NameNode
        requests.post(f"{Config.BASE_URL}/store_metadata", json={"filename": os.path.basename(filename), "blocks": block_ids})

    def get_file(self, filename):
        # Solicitar bloques desde el NameNode
        response = requests.get(f"{Config.BASE_URL}/get_metadata/{filename}")
        if response.status_code == 200:
            block_ids = response.json().get('blocks')
            file_data = bytearray()
            
            for block_id in block_ids:
                with grpc.insecure_channel(Config.DATANODE_URL) as channel:
                    stub = dfs_pb2_grpc.DataNodeStub(channel)
                    block_response = stub.RetrieveBlock(dfs_pb2.RetrieveBlockRequest(block_id=block_id))
                    if block_response.success:
                        file_data.extend(block_response.data)
                    else:
                        print(f"Error recibiendo el bloque {block_id}")
            
            # Guardar el archivo reconstruido
            with open(filename, "wb") as f:
                f.write(file_data)
            print(f"Archivo {filename} guardado.")
        else:
            print(f"Error al obtener los metadatos para {filename}.")

    def ls(self):
        response = requests.get(f"{Config.BASE_URL}/list_files?directory={self.current_directory}")
        if response.status_code == 200:
            files = response.json().get('files', [])
            for file in files:
                print(file)
        else:
            print("Error listando los archivos.")

    def cd(self, directory):
        self.current_directory = directory

    def mkdir(self, directory):
        response = requests.post(f"{Config.BASE_URL}/create_directory", json={"directory": directory})
        if response.status_code == 201:
            print(f"Directorio {directory} creado.")
        else:
            print("Error creando el directorio.")

    def rmdir(self, directory):
        response = requests.delete(f"{Config.BASE_URL}/delete_directory/{directory}")
        if response.status_code == 204:
            print(f"Directorio {directory} removido.")
        else:
            print("Error removiendo el directorio.")

    def rm(self, filename):
        response = requests.delete(f"{Config.BASE_URL}/delete_file/{filename}")
        if response.status_code == 204:
            print(f"Archivo {filename} eliminado.")
        else:
            print("Error eliminando el archivo.")
