# namenode.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Almacenamiento en memoria para los metadatos
file_metadata = {}

@app.route('/store_metadata', methods=['POST'])
def store_metadata():
    data = request.json
    filename = data.get('filename')
    blocks = data.get('blocks')
    
    if not filename or not blocks:
        return jsonify({"error": "Nombre de archivo y bloques son requeridos."}), 400
    
    file_metadata[filename] = blocks
    return jsonify({"message": "Metadatos almacenados exitosamente."}), 201


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
        return jsonify({"message": "Metadatos eliminados exitosamente."}), 204
    return jsonify({"message": "Archivo no encontrado."}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
