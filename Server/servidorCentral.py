import threading
import socket
from ClientThread import ClientThread

# Creamos un socket para el servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("localhost", 5001))

server_socket.listen()

print("Servidor iniciado, esperando conexiones...")

while True:
    # Aceptamos una conexión entrante
    client_socket, client_address = server_socket.accept()
    print(f"Conexión desde {client_address}")

    # Creamos una instancia de la clase ClientThread y le pasamos el socket y la dirección del cliente
    client_thread = ClientThread(client_socket, client_address)
    # Iniciamos el hilo para atender al cliente
    client_thread.start()

# Cerramos el socket del servidor
server_socket.close()

