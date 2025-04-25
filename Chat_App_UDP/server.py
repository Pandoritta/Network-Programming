import socket
import threading
import queue
import time

class UDPServer:
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT

        self.messages = queue.Queue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_socket.bind((self.host, self.port))
        self.clients = {}  
        self.name_to_addr = {} 
        print(f"UDP Server started on {self.host}:{self.port}")

    def start(self):
        threading.Thread(target=self.receive_messages).start()
        threading.Thread(target=self.broadcast_messages).start()

    def send_message_in_private(self, message, sender_name, addr):
        try:
            recipient_name = message[1:].split()[0]
            msg_content = ' '.join(message.split()[1:])
            if recipient_name in self.name_to_addr:
                recipient_addr = self.name_to_addr[recipient_name]
                private_message = f"[Private from {sender_name}]: {msg_content}"
                self.server_socket.sendto(private_message.encode('utf-8'), recipient_addr)
                # Send confirmation to sender
                confirm_message = f"[Private to {recipient_name}]: {msg_content}"
                self.server_socket.sendto(confirm_message.encode('utf-8'), addr)
            else:
                error_msg = f"User {recipient_name} not found!"
                self.server_socket.sendto(error_msg.encode('utf-8'), addr)
        except IndexError:
            error_msg = "Invalid private message format. Use: @username message"
            self.server_socket.sendto(error_msg.encode('utf-8'), addr)
    
    def join_chat(self, addr, message):
        client_name = message[5:]
        self.clients[addr] = client_name
        self.name_to_addr[client_name] = addr
        welcome_msg = f"Welcome {client_name}! Users online: {list(self.clients.values())}"
        self.messages.put((welcome_msg, addr))
        print(f"New client: {client_name} from {addr}")

    def exit_chat(self, addr):
        if addr in self.clients:
            client_name = self.clients[addr]
            del self.name_to_addr[client_name]
            del self.clients[addr]
            self.messages.put((f"{client_name} has left the chat.", None))
            print(f"\033[95mClient \033[0m{client_name}\033[95m has exited from {addr}\033[0m")

    def receive_messages(self):
        while True:
            try:
                data, addr = self.server_socket.recvfrom(1024)
                message = data.decode('utf-8')
                
                if message.startswith("JOIN:"):
                    self.join_chat(addr, message)
                
                elif message.startswith("EXIT:"):
                    self.exit_chat(addr)             
                else:
                    if addr in self.clients:
                        sender_name = self.clients[addr]
                        if message.startswith("@"):
                            self.send_message_in_private(message, sender_name, addr)
                        else:
                            formatted_message = f"{sender_name}: {message}"
                            self.messages.put((formatted_message, None))
            
            except Exception as e:
                print(f"Error: {e}")

    def broadcast_messages(self):
        while True:
            try:
                message, exclude_addr = self.messages.get()
                for client_addr in self.clients:
                    if client_addr != exclude_addr:
                        self.server_socket.sendto(message.encode('utf-8'), client_addr)
                time.sleep(0.1)
            except Exception as e:
                print(f"Broadcast error: {e}")

if __name__ == "__main__":
    server = UDPServer('127.0.0.1', 12345)
    server.start()