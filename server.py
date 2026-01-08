import os
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def recv_data(client_sock):
    data = b""
    while True:
        chunk = client_sock.recv(2048)
        if not chunk:
            break
        data += chunk
        if len(chunk) < 2048:
            break
    return data


def req_handle(client_sock, addr, port):
    try:
        client_sock.settimeout(5)
        data = recv_data(client_sock=client_sock)

        print(f"Received from {addr}: {data.decode()}")

        client_sock.sendall(
            f"Hi from server {port}".encode()
        )

    except socket.timeout:
        print(f"Timeout from {addr}")

    except Exception as e:
        print(f"Error handling {addr}: {e}")

    finally:
        client_sock.close()


if __name__ == "__main__":
    pool = ThreadPoolExecutor(max_workers=os.cpu_count())

    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    port = int(sys.argv[1])
    serv_sock.bind(("0.0.0.0", port))
    serv_sock.listen(128)

    print(f"Server running on port {port}...")

    try:
        while True:
            client_sock, addr = serv_sock.accept()
            print(f"New connection from {addr[0]}:{addr[1]}")
            pool.submit(req_handle, client_sock, addr, port)

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        serv_sock.close()
        pool.shutdown(wait=True)
