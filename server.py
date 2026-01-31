import os
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def receive_data(client_socket):
    data = b""
    while True:
        chunk = client_socket.recv(2048)
        if not chunk:
            break
        data += chunk
        if len(chunk) < 2048:
            break
    return data


def handle_request(client_socket, address, port):
    try:
        client_socket.settimeout(5)
        data = receive_data(client_socket=client_socket)

        print(f"Received from {address}: {data.decode()}")

        client_socket.sendall(
            f"Hi from server {port}".encode()
        )

    except socket.timeout:
        print(f"Timeout from {address}")

    except Exception as e:
        print(f"Error handling {address}: {e}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    pool = ThreadPoolExecutor(max_workers=os.cpu_count())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    port = int(sys.argv[1])
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(128)

    print(f"Server running on port {port}...")

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"New connection from {address[0]}:{address[1]}")
            pool.submit(handle_request, client_socket, address, port)

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()
        pool.shutdown(wait=True)
