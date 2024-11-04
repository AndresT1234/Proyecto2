import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cliente'))

import autenticador
from file_manager import FileManager
from configuracioncliente import CLIENT_ID, DEFAULT_DIRECTORY 

def help():
    print("Comandos disponibles:")
    print(" put <filename>  - Subir un archivo.")
    print(" get <filename>  - Descargar un archivo.")
    print(" ls              - Listar archivos en el directorio actual.")
    print(" cd <directory>  - Cambiar al directorio especificado.")
    print(" mkdir <dir>     - Crear un nuevo directorio.")
    print(" rmdir <dir>     - Eliminar un directorio.")
    print(" rm <filename>   - Eliminar un archivo.")
    print(" exit            - Salir del cliente.")
    print(" help            - Mostrar esta ayuda.")

def main():
    # Autenticación del usuario
    usuario, contraseña = autenticador.obtener_credenciales()
    if not autenticador.autenticar(usuario, contraseña):
        print("Error: Autenticación fallida.")
        return

    file_manager = FileManager(usuario, contraseña) 

    print(f"Bienvenido al Sistema de Archivos Distribuido como {CLIENT_ID}. \n")
    
    # Crear el directorio por defecto si no existe
    if not os.path.exists(DEFAULT_DIRECTORY):
        os.makedirs(DEFAULT_DIRECTORY)

    # Bucle principal del cliente
    while True:
        command = input(f"{file_manager.current_directory}> ").strip().split()
        if not command:
            continue

        cmd = command[0]
        try:
            if cmd == "put" and len(command) > 1:
                file_manager.put_file(command[1])
            elif cmd == "get" and len(command) > 1:
                file_manager.get_file(command[1])
            elif cmd == "ls":
                file_manager.ls()
            elif cmd == "cd" and len(command) > 1:
                file_manager.cd(command[1])
            elif cmd == "mkdir" and len(command) > 1:
                file_manager.mkdir(command[1])
            elif cmd == "rmdir" and len(command) > 1:
                file_manager.rmdir(command[1])
            elif cmd == "rm" and len(command) > 1:
                file_manager.rm(command[1])
            elif cmd == "exit":
                print("Saliendo del cliente.")
                break
            elif cmd == "help":
                help()
            else:
                print("Comando desconocido. Intente nuevamente.")
                print("escriba help -> para ver comandos.")
        except Exception as e:
            print(f"Error: {str(e)}")
            

if __name__ == "__main__":
    main()

