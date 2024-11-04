import requests
import config

def namenode_request(endpoint, data=None):
    """
    Realiza una solicitud HTTP POST al NameNode.
    
    :param endpoint: El endpoint de la API del NameNode.
    :param data: Los datos a enviar como JSON.
    :return: La respuesta del NameNode en formato JSON o None en caso de error.
    """
    url = f"http://{config.NAME_NODE_HOST}:{config.NAME_NODE_PORT}/{endpoint}"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Levanta un error si la respuesta fue un código de error
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud al NameNode: {e}")
        return None  # Retorna None en caso de error

def datanode_request(datanode_address, endpoint, data=None, files=None):
    """
    Realiza una solicitud HTTP POST a un DataNode.
    
    :param datanode_address: Dirección del DataNode.
    :param endpoint: El endpoint de la API del DataNode.
    :param data: Los datos a enviar como JSON.
    :param files: Archivos a enviar.
    :return: La respuesta del DataNode en formato JSON o None en caso de error.
    """
    url = f"http://{datanode_address}/{endpoint}"
    try:
        response = requests.post(url, json=data, files=files)
        response.raise_for_status()  # Levanta un error si la respuesta fue un código de error
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud al DataNode {datanode_address}: {e}")
        return None  # Retorna None en caso de error
