import threading
import socket
import os

# Constante que define el tamaño del buffer de recepción de mensajes
BUFFER_SIZE = 2048

# Creamos una lista para almacenar los archivos disponibles en la red
files = []

class ClientThread(threading.Thread):
    """Clase encargada de atender a un cliente en un hilo separado"""

    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        """Método que se ejecutará en el hilo"""
        # Recibimos mensajes del cliente hasta que se desconecte
        while True:
            # Recibimos el mensaje del cliente
            message = self.client_socket.recv(BUFFER_SIZE).decode()

            # Si el mensaje está vacío, significa que el cliente se ha desconectado
            if not message:
                break

           # Si el mensaje empieza por "SHARE", significa que el cliente quiere compartir un archivo
            if message.startswith("SHARE"):
                # Extraemos el nombre del archivo del mensaje
                file_path = message[6:]

                # Creamos la carpeta "shared_files" si no existe
                os.makedirs("shared_files", exist_ok=True)

                # Obtenemos el nombre del archivo
                file_name = os.path.basename(file_path)

                # Construimos la ruta del archivo en la carpeta "shared_files"
                file_path_in_server = os.path.join("shared_files", file_name)

                # Abrimos el archivo en modo binario para poder leer su contenido
                with open(file_path, "rb") as file_to_send:
                    # Abrimos el archivo en la carpeta "shared_files" en modo escritura binaria para guardar su contenido
                    with open(file_path_in_server, "wb") as file_in_server:
                        # Leemos el contenido del archivo en bloques y lo escribimos en el archivo del servidor
                        chunk = file_to_send.read(BUFFER_SIZE)
                        while chunk:
                            file_in_server.write(chunk)
                            chunk = file_to_send.read(BUFFER_SIZE)


            # Si el mensaje es "REQUEST_FILES", significa que el cliente quiere obtener la lista de archivos disponibles
            elif message == "REQUEST_FILES":
                 # Creamos un mensaje con la lista de archivos disponibles separados por comas
                files_in_folder = os.listdir("shared_files")

                # Creamos un mensaje con la lista de archivos en la carpeta "shared_files" separados por comas
                file_list = ",".join(files_in_folder)

                # Enviamos la lista de archivos al cliente
                self.client_socket.send(file_list.encode())

            elif message == "DISCONECT":
                self.client_socket.close()
                print(f"Cliente desconectado: {self.client_address}")
                break


            # Si el mensaje empieza por "DOWNLOAD", significa que el cliente quiere descargar un archivo
            elif message.startswith("DOWNLOAD"):
                # Extraemos el nombre del archivo del mensaje
                file_name = message[9:]

                # Construimos la ruta del archivo en la carpeta "shared_files"
                file_path = os.path.join("shared_files", file_name)

                # Comprobamos si el archivo existe
                if os.path.isfile(file_path):
                    # Abrimos el archivo en modo binario para poder leer su contenido
                    with open(file_path, "rb") as file_to_send:
                        # Enviamos el tamaño del archivo al cliente
                        file_size = os.path.getsize(file_path)
                        self.client_socket.send(str(file_size).encode())

                        # Leemos el contenido del archivo en bloques y lo enviamos al cliente
                        chunk = file_to_send.read(BUFFER_SIZE)
                        while chunk:
                            self.client_socket.send(chunk)
                            chunk = file_to_send.read(BUFFER_SIZE)
                else:
                    # Enviamos un tamaño de archivo igual a 0 para indicar que el archivo no existe
                    self.client_socket.send(b"0")




