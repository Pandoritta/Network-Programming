import socket
import threading
import sys

class UDPClient:
    def __init__(self, HOST, PORT):
        self.server_addr = (HOST, PORT)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.name = input("Enter your name: ")
        print("\nWelcome! To send a private message, use: @username message")
        print("To exit, type: exit\n")
        
        # Send join message
        join_message = f"JOIN:{self.name}"
        self.client_socket.sendto(join_message.encode('utf-8'), self.server_addr)
        
        # Start receiving thread
        threading.Thread(target=self.receive_messages).start()
        
        # Handle sending messages
        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                data, _ = self.client_socket.recvfrom(1024)
                message = data.decode('utf-8')
                # Color private messages in green, regular messages in blue
                if "[Private" in message:
                    print(f"\033[32m{message}\033[0m")
                else:
                    print(f"\033[34m{message}\033[0m")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_messages(self):
        try:
            while True:
                message = input("")
                if message.lower() == 'exit':
                    self.client_socket.sendto(f"EXIT:{self.name}".encode('utf-8'), self.server_addr)
                    sys.exit()
                self.client_socket.sendto(message.encode('utf-8'), self.server_addr)
        except KeyboardInterrupt:
            self.client_socket.sendto(f"EXIT:{self.name}".encode('utf-8'), self.server_addr)
            sys.exit()

if __name__ == "__main__":
    client = UDPClient('127.0.0.1', 12345)