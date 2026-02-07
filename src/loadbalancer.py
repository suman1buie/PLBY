"""Load balancer module for distributing requests across backend servers."""

from concurrent.futures import ThreadPoolExecutor
import socket
import threading
from read_config import load_config

lock = threading.Lock()
PROXY_SERVER, FORWARD_SERVER_LIST = load_config()
REQUEST_COUNT = 0


def pipe(source, destination):
    """Pipe data from source socket to destination socket."""
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    finally:
        source.close()
        destination.close()


def forward_request_to_server(client_socket):
    """Forward a client request to a backend server using round-robin."""
    try:
        global REQUEST_COUNT  # pylint: disable=global-statement

        with lock:
            backend_server = FORWARD_SERVER_LIST[
                REQUEST_COUNT % len(FORWARD_SERVER_LIST)
            ]
            REQUEST_COUNT += 1
            host, port = backend_server["host"], int(backend_server["port"])

        print(f"Forwarding request to backend localhost:{port}")

        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect((host, port))
        threading.Thread(
            target=pipe, args=(client_socket, backend_socket), daemon=True
        ).start()
        threading.Thread(
            target=pipe, args=(backend_socket, client_socket), daemon=True
        ).start()

        print("Response sent back to client")

    except OSError as e:
        print("Error:", e)


def run_proxy_server():
    """Start the proxy server and listen for incoming connections."""
    pool = ThreadPoolExecutor(max_workers=4)
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
    )
    proxy_host = PROXY_SERVER.get("host", "0.0.0.0")
    proxy_port = int(PROXY_SERVER.get("port", 8000))
    load_balancer_socket.bind((proxy_host, proxy_port))
    load_balancer_socket.listen(128)

    print(f"Load balancer listening on port {proxy_port}...")

    while True:
        client_socket, address = load_balancer_socket.accept()
        print(f"Request coming from {address[0]}:{address[1]}")
        pool.submit(forward_request_to_server, client_socket)


if __name__ == "__main__":
    run_proxy_server()
