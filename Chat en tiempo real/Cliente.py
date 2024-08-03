import socket # Importa el módulo de sockets.
import threading #Importa el módulo de hilos, que permite ejecutar varias tareas simultáneamente.
import sys #Importa el módulo del sistema, utilizado para salir del programa.

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 12345

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("El servidor se ha cerrado")
                client_socket.close()
                sys.exit() #Sale del programa si ocurre un error o se cierra la conexión.

        except:
            print("Error al recibir el mensaje")
            client_socket.close()
            sys.exit()

def start_client():
    # Crear el socket del cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Iniciar el hilo para recibir mensajes
    # Crea un hilo para ejecutar la función receive_messages que manejará la recepción de mensajes en paralelo.
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Enviar mensajes desde la terminal
    while True:
        message = input()
        if message:
            client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_client()
