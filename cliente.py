import socket
import os

# Creamos un socket para el cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Constante que define el tamaño del buffer de recepción de mensajes
BUFFER_SIZE = 2048

# Nos conectamos al servidor
client_socket.connect(("localhost", 5001))

# Enviamos un mensaje al servidor
client_socket.send("HOLA SERVIDOR".encode())

while True:
    # Mostramos un menú de opciones al usuario
    print("¿Qué quieres hacer?")
    print("1. Compartir un archivo")
    print("2. Obtener la lista de archivos disponibles")
    print("3. Descargar un fichero")
    print("4. Desconectarse del servidor")

    # Leemos la opción seleccionada por el usuario
    option = input()

    # Si la opción es "1", significa que el usuario quiere compartir un archivo
    if option == "1":
       # Leemos la ruta del archivo
        file_path = input("Introduce la ruta del archivo: ")

        # Creamos el mensaje "SHARE" con el nombre y el contenido del archivo
        message = f"SHARE {file_path}"

        # Enviamos el mensaje al servidor
        client_socket.send(message.encode())

    # Si la opción es "2", significa que el usuario quiere obtener la lista de archivos disponibles
    elif option == "2":
        # Enviamos el mensaje "REQUEST_FILES" al servidor
        client_socket.send("REQUEST_FILES".encode())

        # Recibimos la respuesta del servidor (la lista de archivos disponibles)
        file_list = client_socket.recv(BUFFER_SIZE).decode()
        print("Archivos disponibles:", file_list)

    # Si el usuario elige la opción "3", significa que quiere descargar un archivo
    elif option == "3":
        # Pedimos al usuario que indique el nombre del archivo que quiere descargar
        file_name = input("Indica el nombre del archivo que quieres descargar: ")

        # Enviamos un mensaje al servidor solicitando el archivo
        client_socket.send(("DOWNLOAD " + file_name).encode())

        # Recibimos el tamaño del archivo
        file_size = int(client_socket.recv(BUFFER_SIZE).decode())

        # Si el tamaño del archivo es mayor que 0, significa que el archivo existe y lo podemos descargar
        if file_size > 0:
            # Abrimos un archivo en modo escritura binaria para guardar el contenido del archivo descargado
            with open(file_name, "wb") as file:
                # Recibimos el archivo en bloques y lo escribimos en el archivo que hemos abierto
                while file_size > 0:
                    chunk = client_socket.recv(BUFFER_SIZE)
                    file.write(chunk)
                    file_size -= len(chunk)
            print("El archivo se ha descargado correctamente")
        else:
            print("El archivo no se encuentra disponible en el servidor")

    # Si la opción es "4", significa que el usuario quiere desconectarse
    elif option == "4":
        # Enviamos el mensaje "DISCONECT" al servidor
        client_socket.send("DISCONECT".encode())
        break


# Recibimos una respuesta del servidor
response = client_socket.recv(1024).decode()

# Mostramos la respuesta del servidor
print(response)

# Cerramos el socket del cliente
client_socket.close()
