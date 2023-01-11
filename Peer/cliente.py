import socket
import os

# Creamos un socket para el cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

BUFFER_SIZE = 2048

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
    print("5. Consultar el espacio disponible en el servidor")
    print("6. Desconectarse del servidor")

    option = input()


    # Si la opción es "1", significa que el usuario quiere compartir un archivo
    if option == "1":
        file_path = input("Introduce la ruta del archivo: ")

        message = f"SHARE {file_path}"

        client_socket.send(message.encode())
        print(client_socket.recv(BUFFER_SIZE).decode())



    # Si la opción es "2", significa que el usuario quiere obtener la lista de archivos disponibles
    if option == "2":
        client_socket.send("REQUEST_FILES".encode())

        file_list = client_socket.recv(BUFFER_SIZE).decode()
        print(file_list)


    # Si el usuario elige la opción "3", significa que quiere descargar un archivo
    if option == "3":
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

        if file_size > 0:
            with open(selected_filename, "wb") as file:
                while file_size > 0:
                    chunk = client_socket.recv(BUFFER_SIZE)
                    file.write(chunk)
                    file_size -= len(chunk)
            print("El archivo se ha descargado correctamente")
        else:
            print("El archivo no se encuentra disponible en el servidor")

    # Si la opción es "5", significa que el usuario quiere desconectarse
    if option == "6":
        client_socket.send("DISCONNECT".encode())
        break

    # Si la opción es "4", significa que el usuario quiere conocer el estado de los otros clientes.
    if option == "4":
        client_socket.send("REQUEST_CLIENTS_STATUS".encode())

        usuarios = client_socket.recv(BUFFER_SIZE).decode()
        usuarios = usuarios.split(",")
        print("Los usuarios que están conectados actualmente son: ")
        for usuario in usuarios:
            print(usuario)

    # Si la opción es "5", significa que el usuario quiere desconectarse
    if option == "5":
        client_socket.send("REQUEST_STORAGE_INFO".encode())

        storage_info_message = client_socket.recv(BUFFER_SIZE).decode()
        print(f"El tamaño disponible en el servidor es: {storage_info_message} GB")




response = client_socket.recv(1024).decode()

print(response)

client_socket.close()