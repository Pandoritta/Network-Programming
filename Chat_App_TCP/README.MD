# TCP Chat Application

A simple TCP-based chat application implemented in Python that allows multiple clients to communicate through a central server.

## Features

- Multi-client support
- Real-time messaging
- Colored message display for received messages
- Support for client join/leave notifications
- Clean exit functionality

## Components

- `a_server.py` - TCP server implementation
- `client.py` - TCP client implementation

## Requirements

- Python 3.x
- Socket library (built-in)
- Threading library (built-in)

## Usage

### Starting the Server

1. Run the server script:
```bash
python a_server.py
```
The server will start on localhost (127.0.0.1) port 12345

### Connecting Clients

1. Run the client script:
```bash
python client.py
```
2. Enter your name when prompted
3. Start chatting!

### Chat Commands

- Type your message and press Enter to send
- Type 'exit' to leave the chat

## Technical Details

- Uses TCP sockets for reliable communication
- Implements threading for handling multiple client connections
- Supports UTF-8 encoding for messages
- Maximum 5 concurrent client connections
- Buffer size: 1024 bytes
