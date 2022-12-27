import socket
import os

# Creamos un socket para el cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Constante que define el tamaño del buffer de recepción de mensajes
BUFFER_SIZE = 2048

# Nos conectamos al servidor
client_socket.connect(("localhost", 5001))

nombre = input("Introduce un nombre de usuario: ")

client_socket.send(nombre.encode())

while True:
    # Mostramos un menú de opciones al usuario
    print("¿Qué quieres hacer?")
    print("1. Compartir un archivo")
    print("2. Obtener la lista de archivos disponibles")
    print("3. Descargar un fichero")
    print("4. Consultar los usuarios conectados")
    print("5. Desconectarse del servidor")

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
        client_socket.send("REQUEST_DOWNLOAD".encode())
        file_list = client_socket.recv(BUFFER_SIZE).decode()
        files = file_list.split(",")

        print("Selecciona el archivo que deseas descargar:")
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")

        selected_file = input()
        selected_file = int(selected_file)
        selected_filename = files[selected_file-1]
        print(selected_filename)
        client_socket.send(("DOWNLOAD " + selected_filename).encode())
        file_size = client_socket.recv(BUFFER_SIZE).decode()
        file_size = int(file_size)

        # Si el tamaño del archivo es mayor que 0, significa que el archivo existe y lo podemos descargar
        if file_size > 0:
            # Abrimos un archivo en modo escritura binaria para guardar el contenido del archivo descargado
            with open(selected_filename, "wb") as file:
                # Recibimos el archivo en bloques y lo escribimos en el archivo que hemos abierto
                while file_size > 0:
                    chunk = client_socket.recv(BUFFER_SIZE)
                    file.write(chunk)
                    file_size -= len(chunk)
            print("El archivo se ha descargado correctamente")
        else:
            print("El archivo no se encuentra disponible en el servidor")

    # Si la opción es "5", significa que el usuario quiere desconectarse
    elif option == "5":
        # Enviamos el mensaje "DISCONNECT" al servidor
        client_socket.send("DISCONNECT".encode())
        break

    elif option == "6":
        # Enviamos un mensaje al servidor pidiendo la lista de clientes y su estado de conexión
        client_socket.send("REQUEST_CLIENTS_STATUS".encode())

        # Recibimos la respuesta del servidor con la lista de clientes y su estado de conexión
        usuarios = client_socket.recv(BUFFER_SIZE).decode()
        usuarios = usuarios.split(",")
        print("Los usuarios que están conectados actualmente son: ")
        # Mostramos la lista de clientes y su estado de conexión en pantalla
        for usuario in usuarios:
            print(usuario)

    elif option == "7":
        client_socket.send("REQUEST_STORAGE_INFO".encode())

        storage_info_message = client_socket.recv(BUFFER_SIZE).decode()
        print(f"El tamaño disponible en el servidor es: {storage_info_message} GB")
        


# Recibimos una respuesta del servidor
response = client_socket.recv(1024).decode()

# Mostramos la respuesta del servidor
print(response)

# Cerramos el socket del cliente
client_socket.close()