# UDP Chat Application

A real-time chat application implemented using UDP protocol in Python, supporting both public and private messaging.

## Features

- Multi-client support
- Private messaging between users
- Join/Leave notifications
- Online users list
- Graceful exit handling

## Requirements

- Python 3.x
- Standard library modules:
  - socket
  - threading
  - queue
  - time


### Starting the Server

1. Open terminal and run:
```bash
python3 server.py
```
The server will start on localhost (127.0.0.1) port 12345

### Connecting Clients

1. Open a new terminal window for each client:
```bash
python3 client.py
```
2. Enter your username when prompted
3. Start chatting!

### Chat Commands

- **Public Message**: Simply type your message and press Enter
- **Private Message**: Use `@username message`
  ```
  @john Hey, how are you?
  ```
- **Exit Chat**: Type `exit` and press Enter

## Project Structure

```
Chat_App_UDP/
├── server.py      
├── client.py      
└── README.md      
```