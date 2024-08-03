import socket # Importa el módulo de sockets, que proporciona funciones para crear y usar conexiones de red.
import select #Importa el módulo select, que permite manejar múltiples conexiones al mismo tiempo de manera eficiente.

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 12345

def start_server():

    # Crear el socket del servidor

    #Crea un socket TCP/IP. AF_INET indica que se utilizará IPv4, y SOCK_STREAM indica que es un socket de flujo (TCP).
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Configura la opción para reutilizar la dirección. Esto es útil para evitar errores si el socket se cierra y se vuelve a abrir rápidamente.

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Asocia el socket a una dirección IP y puerto específicos. Aquí, el servidor escuchará en 127.0.0.1:12345.
    server_socket.bind((HOST, PORT))

    #Configura el socket para escuchar conexiones entrantes. El número 5 es la cantidad máxima de conexiones en espera.
    server_socket.listen(5)
    
    # Lista de sockets a gestionar
    sockets_list = [server_socket] #Lista que mantiene todos los sockets a los que el servidor está atento. Inicialmente solo incluye el socket del servidor.
    clients = {}

    print("Servidor de chat iniciado en {}:{}".format(HOST, PORT))


    while True:
        # Usar select para manejar múltiples conexiones
        readable, _, _ = select.select(sockets_list, [], []) # select monitoriza los sockets en sockets_list para ver cuáles están listos para leer. El segundo y tercer argumentos son para escribir y manejar excepciones, respectivamente, pero los dejamos vacíos.

        for notified_socket in readable:
            if notified_socket == server_socket:
                # Nueva conexión
                client_socket, client_address = server_socket.accept() #cepta una nueva conexión entrante. Devuelve un nuevo socket para la conexión y la dirección del cliente.

                sockets_list.append(client_socket)
                clients[client_socket] = client_address
                print("Nuevo cliente conectado:", client_address)

            else:
                # Mensaje de un cliente
                try:
                    message = notified_socket.recv(1024).decode('utf-8') #Lee hasta 1024 bytes del socket

                    if message:
                        # Broadcast del mensaje a todos los clientes

                        print("Mensaje recibido:", message)
                        for client_socket in clients:
                            if client_socket != notified_socket:
                                client_socket.send(message.encode('utf-8'))
                    else:
                        # Cliente desconectado
                        print("Cliente desconectado:", clients[notified_socket])
                        
                        #Elimina el socket del cliente que se ha desconectado de la lista de sockets y del diccionario de clientes.
                        sockets_list.remove(notified_socket)

                        del clients[notified_socket]
                except:
                    print("Error al recibir el mensaje")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]

if __name__ == "__main__":
    start_server()
