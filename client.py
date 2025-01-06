import socket
import threading
import time
from pydub import AudioSegment
import simpleaudio as sa


def client(server_ip='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print(f"Connected to server at {server_ip}:{port}")

    stop_flags = {}
    playback_objects = {}
    playing_threads = {}

    def play_audio(audio_file, repeat=False):
        try:
            audio = AudioSegment.from_file(audio_file, format="m4a")
            while True:
                if audio_file in stop_flags and stop_flags[audio_file]:
                    print(f"Stopping playback for {audio_file}")
                    break
                playback = sa.play_buffer(audio.raw_data,
                                          num_channels=audio.channels,
                                          bytes_per_sample=audio.sample_width,
                                          sample_rate=audio.frame_rate)
                playback_objects[audio_file] = playback
                playback.wait_done()
                if not repeat:
                    break
        except Exception as e:
            print(f"Error playing audio: {e}")

    def stop_audio(audio_file):
        if audio_file in stop_flags:
            stop_flags[audio_file] = True
        if audio_file in playback_objects and playback_objects[audio_file].is_playing():
            playback_objects[audio_file].stop()
        if audio_file in playing_threads:
            playing_threads[audio_file].join()
            del playing_threads[audio_file]

    def receive_commands():
        client_socket.sendall(b'READY')

        def play_audio_in_thread(audio_file, repeat):
            stop_flags[audio_file] = False
            thread = threading.Thread(target=play_audio, args=(audio_file, repeat))
            thread.start()
            playing_threads[audio_file] = thread

        while True:
            command = client_socket.recv(1024).decode()
            if command.startswith("PLAY"):
                parts = command.split(" ", 2)
                audio_file = parts[1]
                repeat = len(parts) > 2 and parts[2] == "REPEAT"
                play_audio_in_thread(audio_file, repeat)
            elif command.startswith("STOP"):
                parts = command.split(" ", 1)
                audio_file = parts[1]
                stop_audio(audio_file)

    receive_commands()

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



