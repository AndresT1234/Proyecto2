import getpass

def obtener_credenciales():
    usuario = input("Usuario: ")
    contraseña = getpass.getpass("Contraseña: ")
    return usuario, contraseña

def autenticar(usuario, contraseña):
    usuarios_permitidos = {"admin": "1234"}
    if usuario in usuarios_permitidos and usuarios_permitidos[usuario] == contraseña:
        print("\nAutenticación exitosa.\n")
        return True
    else:
        print("Error: Usuario o contraseña incorrectos.")
        return False
