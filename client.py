import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Message: {message.decode()}")
        except:
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))
    
    see_existing = input("See existing chat rooms? yes/no: ").strip().lower()
    client_socket.send(see_existing.encode())
    
    if see_existing == "yes":
        available_rooms = client_socket.recv(1024).decode()
        print(available_rooms)
    
    room = input("Enter room name: ").strip()
    client_socket.send(room.encode())
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode())
    
    client_socket.close()

if __name__ == "__main__":
    start_client()
