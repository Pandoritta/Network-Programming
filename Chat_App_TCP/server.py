import socket
from threading import Thread


class Server():
    """This class implements a TCP server that can handle multiple clients.
    It listens for incoming connections, accepts them, and starts a new thread
    for each client to handle communication.
    """
    #List of connected clients
    Clients = []

    #Constructor TCP socket (bind to host and port and listen for incoming connections)
    def __init__(self, HOST, PORT):
        """This method initializes the server by creating a socket, binding it to
        the specified host and port, and starting to listen for incoming connections.
        Args:
            HOST (str): The host address to bind the server to.
            PORT (int): The port number to bind the server to.
        """
        self.HOST = HOST
        self.PORT = PORT
        self.server = socket.socket()
        self.server.bind((self.HOST, self.PORT)) 
        self.server.listen(5) #maximum amount of clients that can connect at the same time
        print(f"Server started on {self.HOST}:{self.PORT}")

    def listen(self):
        """This method listens for incoming connections and starts a new thread
        for each client to handle communication.
        It accepts the client connection, receives the client's name, and adds
        the client to the list of connected clients.
        It also broadcasts a message to all clients that a new client has joined.
        """
        while True:
            client, address = self.server.accept()
            print(f"Connection from {address} has been established!")
            
            client_name = client.recv(1024).decode('utf-8')
            client = {'client_name': client_name, 'client_socket': client}

            self.broadcast(client_name, client_name + " has joined the chat!")
            Server.Clients.append(client)
            Thread(target=self.handle_new_client, args=(client,)).start()
            
    def handle_new_client(self, client):
        """This method handles communication with a new client.
        It receives messages from the client and broadcasts them to all other clients.
        If the client sends an 'exit' message, it closes the connection and removes
        the client from the list of connected clients.
        Args:
            client (dict): A dictionary containing the client's name and socket.
        """
        client_name = client['client_name']
        client_socket = client['client_socket']

        while True:

            client_message = client_socket.recv(1024).decode('utf-8')

            if 'exit' in client_message.lower():
                self.broadcast(client_name, f"{client_name}" + " has left the chat!")
                Server.Clients.remove(client)
                client_socket.close()
                print(f"Connection from {client_name} has been removed!")
                break
            else:
                self.broadcast(client_name, client_message)

    def broadcast(self, sender_name, message):
        for client in self.Clients:
            client_socket = client['client_socket']
            client_name = client['client_name']
            if client_name != sender_name:
                client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    server = Server('127.0.0.1', 12345)
    server.listen()