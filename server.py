import socket
import threading
import time
from pydub import AudioSegment
import simpleaudio as sa

def server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    clients = {}
    client_counter = 1  # To assign unique IDs to clients

    def handle_client(client_socket, client_id):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message == 'READY':
                    print(f"Client {client_id} ready: {client_socket.getpeername()}")
            except ConnectionResetError:
                break
        client_socket.close()
        del clients[client_id]

    def accept_clients():
        nonlocal client_counter
        while True:
            client_socket, addr = server_socket.accept()
            client_id = client_counter
            client_counter += 1
            clients[client_id] = client_socket
            print(f"New connection from {addr}, assigned Client ID: {client_id}")
            threading.Thread(target=handle_client, args=(client_socket, client_id)).start()

    accept_thread = threading.Thread(target=accept_clients)
    accept_thread.start()

    # Keyboard bindings to audio files
    audio_bindings = {
        'a': ('background.m4a', True),  # Play on repeat
        'b': ('error.m4a', False),
        'c': ('test_audio.m4a', True),
        'd': ('test4.mp3', False),
        'e': ('test5.mp3', False),
        'f': ('test6.mp3', False),
        'g': ('test7.mp3', False),
        'h': ('test8.mp3', False),
        'i': ('test9.mp3', False),
        'j': ('test10.mp3', False),
    }

    active_audio = {}

    while True:
        command = input("Enter target clients and key (e.g., '12a') or 'x' to shut down: ").strip()
        if command.lower() == 'x':
            print("Shutting down server...")
            break
        elif len(command) > 1 and command[-1] in audio_bindings:
            target_clients = command[:-1]
            audio_file, repeat = audio_bindings[command[-1]]
            print(f"Broadcasting PLAY command for {audio_file} {'on repeat' if repeat else ''} to clients {target_clients}")
            for client_id in target_clients:
                if client_id.isdigit():
                    client_id = int(client_id)
                    if client_id in clients:
                        clients[client_id].sendall(f"PLAY {audio_file} {'REPEAT' if repeat else ''}".encode())
                        active_audio[(client_id, audio_file)] = repeat
                    else:
                        print(f"Client {client_id} not connected.")
        elif len(command) > 1 and command[-1] == 's':  # 's' to stop audio
            target_clients = command[:-1]
            for client_id in target_clients:
                if client_id.isdigit():
                    client_id = int(client_id)
                    if client_id in clients:
                        for (cid, audio_file), _ in list(active_audio.items()):
                            if cid == client_id:
                                clients[client_id].sendall(f"STOP {audio_file}".encode())
                                del active_audio[(cid, audio_file)]
                    else:
                        print(f"Client {client_id} not connected.")
        else:
            print("Invalid input. Please enter a valid key.")

    for client in clients.values():
        client.close()
    server_socket.close()
    accept_thread.join()
    print("Server closed.")

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        server()
    elif len(sys.argv) > 1 and sys.argv[1] == 'client':
        server_ip = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
        client(server_ip=server_ip)
    else:
        print("Usage: python script.py server or python script.py client [server_ip]")

