import os
import sys
from autenticador import autenticar
from configuracioncliente import DEFAULT_DIRECTORY

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Comm'))
from Comm import protocol, config

class FileManager:
    def __init__(self, usuario=None, contraseña=None):
        self.usuario = usuario
        self.contraseña = contraseña
        self.current_directory = DEFAULT_DIRECTORY

    def authenticate(self):
        return autenticar(self.usuario, self.contraseña)

    def handle_request_error(self, response, context):
        if response and not response.get("success"):
            print(f"Error en {context}: {response.get('message', 'Error desconocido')}")
            return True
        return False

    def put_file(self, filename):
        try:
            with open(filename, "rb") as f:
                file_data = f.read()
        except FileNotFoundError:
            print(f"Error: El archivo '{filename}' no se encontró.")
            return
        except PermissionError:
            print(f"Error: Permiso denegado para leer el archivo '{filename}'.")
            return
        except Exception as e:
            print(f"Error al leer el archivo '{filename}': {e}")
            return

        # Dividir el archivo en bloques
        block_size = config.BLOCK_SIZE
        blocks = [file_data[i:i + block_size] for i in range(0, len(file_data), block_size)]
        block_ids = []

        for i, block in enumerate(blocks):
            block_id = f"{os.path.basename(filename)}_block_{i}"
            block_ids.append(block_id)

            response = protocol.datanode_request(
                datanode_address=config.DATA_NODE_HOSTS[0],
                endpoint="StoreBlock",
                data={"block_id": block_id, "data": block}
            )
            if self.handle_request_error(response, f"almacenamiento del bloque {block_id}"):
                return

        metadata_response = protocol.namenode_request(
            endpoint="store_metadata",
            data={"filename": os.path.basename(filename), "blocks": block_ids}
        )
        if metadata_response and metadata_response.get("message"):
            print(metadata_response["message"])
        else:
            print(f"Error al registrar metadatos para '{filename}'.")

    def get_file(self, filename):
        response = protocol.namenode_request(f"get_metadata/{filename}")
        if response and "blocks" in response:
            block_ids = response["blocks"]
            file_data = bytearray()

            for block_id in block_ids:
                block_response = protocol.datanode_request(
                    datanode_address=config.DATA_NODE_HOSTS[0],
                    endpoint="RetrieveBlock",
                    data={"block_id": block_id}
                )
                if self.handle_request_error(block_response, f"recepción del bloque '{block_id}'"):
                    return
                file_data.extend(block_response["data"])

            with open(filename, "wb") as f:
                f.write(file_data)
            print(f"Archivo '{filename}' descargado exitosamente.")
        else:
            print(f"Error al obtener los metadatos para '{filename}'.")

    def ls(self):
        response = protocol.namenode_request("list_files", method='GET')
        if response and "files" in response:
            files = response["files"]
            if files:
                print("Archivos en el sistema de archivos distribuido:")
                for file in files:
                    print(f" - {file}")
            else:
                print("No hay archivos en el sistema.")
        else:
            print("Error al listar los archivos.")

    def cd(self, directory):
        new_directory = os.path.join(self.current_directory, directory)  
        if os.path.isdir(new_directory):
            self.current_directory = new_directory
            print(f"Directorio cambiado a '{self.current_directory}'.")
        else:
            print(f"Error: El directorio '{new_directory}' no existe.")

    def mkdir(self, directory):
        new_directory = os.path.join(self.current_directory, directory)
        # Verifica que el directorio padre existe
        if not os.path.isdir(self.current_directory):
            print(f"Error: El directorio padre '{self.current_directory}' no existe.")
            return

        response = protocol.namenode_request(
            endpoint="create_directory",
            data={"directory": new_directory}
        )
        if response and response.get("message"):
            print(response["message"])
        else:
            print(f"Error al crear el directorio '{new_directory}'.")

    def rmdir(self, directory):
        response = protocol.namenode_request(f"delete_directory/{directory}") 
        if response and response.get("message"):
            print(response["message"])
        else:
            print(f"Error al eliminar el directorio '{directory}'.")

    def rm(self, filename):
        file_to_remove = os.path.join(self.current_directory, filename)  
        response = protocol.namenode_request(f"delete_file/{file_to_remove}")
        if response and response.get("message"):
            print(response["message"])
        else:
            print(f"Error al eliminar el archivo '{file_to_remove}'.")

