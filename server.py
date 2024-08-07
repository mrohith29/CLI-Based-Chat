import socket
import threading

rooms = {}
clients = {}

def broadcast(message, room, sender_socket):
    for client in rooms[room]:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                rooms[room].remove(client)

def handle_client(client_socket, room):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, room, client_socket)
        except:
            client_socket.close()
            rooms[room].remove(client_socket)
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        # client_socket.send(b"Enter room name: ")
        room = client_socket.recv(1024).decode().strip()
        
        if room not in rooms:
            rooms[room] = []
        rooms[room].append(client_socket)
        
        print(f"Connection from {addr} to room {room}")
        threading.Thread(target=handle_client, args=(client_socket, room)).start()

if __name__ == "__main__":
    start_server()
