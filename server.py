import socket
import threading

rooms = {}
lock = threading.Lock()

def avail_rooms(client_socket):
    available = "The available rooms are: "
    if rooms:
        available += ", ".join(rooms.keys())
    else:
        available += "No active rooms available."
    client_socket.send(available.encode())

def broadcast(message, room, sender_socket):
    with lock:
        for client in rooms.get(room, []):
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
            break
    with lock:
        client_socket.close()
        if room in rooms:
            rooms[room].remove(client_socket)
            if not rooms[room]:
                del rooms[room]

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        see_rooms = client_socket.recv(1024).decode().strip()
        if see_rooms == "yes":
            avail_rooms(client_socket)
        
        room = client_socket.recv(1024).decode().strip()
        with lock:
            if room not in rooms:
                rooms[room] = []
            rooms[room].append(client_socket)
        
        print(f"Connection from {addr} to room {room}")
        threading.Thread(target=handle_client, args=(client_socket, room)).start()

if __name__ == "__main__":
    start_server()
