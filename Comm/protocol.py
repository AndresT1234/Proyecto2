# protocol.py
import requests
import config

def handle_request_error(e, context):
    if isinstance(e, requests.exceptions.HTTPError):
        print(f"Error HTTP en la solicitud al {context}: {e}")
    elif isinstance(e, requests.exceptions.ConnectionError):
        print(f"Error de conexión con el {context}. Verifique la dirección.")
    elif isinstance(e, requests.exceptions.Timeout):
        print(f"La solicitud al {context} ha superado el tiempo de espera.")
    else:
        print(f"Error en la solicitud al {context}: {e}")

def namenode_request(endpoint, data=None, method='POST'):
    url = f"http://{config.NAME_NODE_HOST}:{config.NAME_NODE_PORT}/{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'DELETE': 
            response = requests.delete(url, json=data) 
        else:
            response = requests.post(url, json=data)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        handle_request_error(e, f"NameNode en '{endpoint}'")
    return None

def datanode_request(datanode_address, endpoint, data=None):
    url = f"http://{datanode_address}/{endpoint}"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  
        return response.json()
    except Exception as e:
        handle_request_error(e, f"DataNode en {datanode_address} para '{endpoint}'")
    return None
