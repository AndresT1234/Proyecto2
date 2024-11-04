import shutil
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Almacenamiento en memoria para los metadatos
file_metadata = {}

@app.route('/store_metadata', methods=['POST'])
def store_metadata():
    try:
        data = request.json
        filename = data.get('filename')
        blocks = data.get('blocks')
        
        if not filename or not isinstance(blocks, list):
            return jsonify({"error": "El nombre de archivo y los bloques (en lista) son requeridos."}), 400
        
        file_metadata[filename] = blocks
        return jsonify({"message": "Metadatos almacenados exitosamente."}), 201
    except Exception as e:
        return jsonify({"error": f"Error al almacenar metadatos: {str(e)}"}), 500

@app.route('/get_metadata/<filename>', methods=['GET'])
def get_metadata(filename):
    blocks = file_metadata.get(filename)
    if blocks is not None:
        return jsonify({"blocks": blocks}), 200
    return jsonify({"message": "Archivo no encontrado."}), 404

@app.route('/list_files', methods=['GET'])
def list_files():
    return jsonify({"files": list(file_metadata.keys())}), 200

@app.route('/delete_metadata/<filename>', methods=['DELETE'])
def delete_metadata(filename):
    if filename in file_metadata:
        del file_metadata[filename]
        return jsonify({"message": "Metadatos eliminados exitosamente."}), 200
    return jsonify({"message": "Archivo no encontrado."}), 404

@app.route('/create_directory', methods=['POST'])
def create_directory():
    data = request.json
    directory_name = data.get('directory')

    if not directory_name:
        return jsonify({"error": "Se requiere un nombre de directorio."}), 400

    if directory_name in file_metadata:
        return jsonify({"error": "El directorio ya existe."}), 400

    try:
        os.makedirs(directory_name, exist_ok=True)

        file_metadata[directory_name] = {
            "type": "directory",
            "contents": []
        }

        file_metadata[directory_name] = [] 
        return jsonify({"message": f"Directorio '{directory_name}' creado."}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el directorio: {str(e)}"}), 500

@app.route('/delete_directory/<directory>', methods=['DELETE'])
def delete_directory(directory):
    if directory in file_metadata:
        try:
            shutil.rmtree(directory)  # Elimina el directorio y su contenido
            del file_metadata[directory]
            return jsonify({"message": "Directorio eliminado exitosamente."}), 200
        except OSError as e:
            return jsonify({"error": f"Error al eliminar el directorio: {str(e)}"}), 500
    return jsonify({"message": "Directorio no encontrado."}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
