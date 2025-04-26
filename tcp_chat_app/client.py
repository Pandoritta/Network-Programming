import socket
from threading import Thread

import os

class Client():

    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.socket = socket.socket()
        self.socket.connect((self.HOST, self.PORT))
        self.name = input("Enter your name: ")
        
        self.talk_to_server()

    def talk_to_server(self):
        self.socket.send(self.name.encode('utf-8'))
        Thread(target=self.receive_message).start()
        self.send_message()
        
    def send_message(self):
        while True: 
            client_input = input("")
            client_message =   self.name + ": " + client_input
            self.socket.send(client_message.encode('utf-8'))

    def receive_message(self):
        while True:
            server_message = self.socket.recv(1024).decode('utf-8')
            if not server_message.strip():
                os._exit(0)
            print("\033[34m" + server_message + "\033[0m")

if __name__ == "__main__":
    Client('127.0.0.1', 12345)