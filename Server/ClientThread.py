import threading
import socket
import os
import psutil

# Constante que define el tamaño del buffer de recepción de mensajes
BUFFER_SIZE = 2048

# Diccionario para almacenar la información de los clientes conectados
clients = {}


class ClientThread(threading.Thread):
    """Clase encargada de atender a un cliente en un hilo separado"""

    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        """Método que se ejecutará en el hilo"""
        nombre = self.client_socket.recv(BUFFER_SIZE).decode()
        client_address = self.client_address
        clients[client_address] = {"ip": client_address[0], "port": client_address[1], "status": "connected", "usuario": nombre}

        while True:
            message = self.client_socket.recv(BUFFER_SIZE).decode()

            if not message:
                break

            if message.startswith("SHARE"):
                # Extraemos el nombre del archivo del mensaje
                file_path = message[6:]

                if os.path.isfile(file_path):

                    os.makedirs("shared_files", exist_ok=True)

                    file_name = os.path.basename(file_path)

                    file_path_in_server = os.path.join("shared_files", file_name)

                    # Abrimos el archivo en modo binario para poder leer su contenido
                    with open(file_path, "rb") as file_to_send:

                        with open(file_path_in_server, "wb") as file_in_server:
                            chunk = file_to_send.read(BUFFER_SIZE)
                            while chunk:
                                file_in_server.write(chunk)
                                chunk = file_to_send.read(BUFFER_SIZE)

                    self.client_socket.send(b"El fichero se ha compartido con el servidor correctamente.")

                else:
                    self.client_socket.send(b"Esa ruta no es valida para el archivo.")


            elif message == "REQUEST_FILES":
                files_in_folder = os.listdir("shared_files")

                if len(files_in_folder) == 0:
                    self.client_socket.send("No hay archivos en el servidor".encode())

                file_list = ",".join(files_in_folder)

                self.client_socket.send(file_list.encode())

            elif message == "REQUEST_DOWNLOAD":
                files_in_folder = os.listdir("shared_files")

                file_list = ",".join(files_in_folder)

                self.client_socket.send(file_list.encode())

            elif message == "DISCONNECT":
                clients[self.client_address] = {"ip": self.client_address, "port": self.client_address, "status": "disconnected"}
                self.client_socket.close()
                print(f"Cliente desconectado: {self.client_address}")
                break


            elif message.startswith("DOWNLOAD"):
                # Extraemos el nombre del archivo del mensaje
                file_name = message[9:]

                file_path = os.path.join("shared_files", file_name)

                # Comprobamos si el archivo existe
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as file_to_send:
                        file_size = os.path.getsize(file_path)
                        self.client_socket.send(str(file_size).encode())

                        # Leemos el contenido del archivo en bloques y lo enviamos al cliente
                        chunk = file_to_send.read(BUFFER_SIZE)
                        while chunk:
                            self.client_socket.send(chunk)
                            chunk = file_to_send.read(BUFFER_SIZE)
                else:
                    self.client_socket.send(b"0")

            elif message == "REQUEST_CLIENTS_STATUS":
                connected_clients = []
                for client in clients:
                    if clients[client]["status"] == "connected":
                        connected_clients.append(f"{clients[client]['usuario']} - {clients[client]['status']}")
                clients_list = ",".join(connected_clients)

                self.client_socket.send(clients_list.encode())

            elif message == "REQUEST_STORAGE_INFO":

                disk = psutil.disk_usage("shared_files")

                # Calculamos el espacio disponible en GB
                available_space_mb = disk.free / (1024 * 1024 * 1024)

                available_space_mb = round(available_space_mb, 2)

                self.client_socket.send(str(available_space_mb).encode())




