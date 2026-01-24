from concurrent.futures import ThreadPoolExecutor
import socket
import threading
from read_config import load_config

lock = threading.Lock()
PROXY_SERVER, FORWORD_SERVER_LIST = load_config()
cnt = 0


def pipe(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    finally:
        src.close()
        dst.close()


def forward_request_to_server(client_socket):
    try:
        global cnt

        with lock:
            _server = FORWORD_SERVER_LIST[cnt % len(FORWORD_SERVER_LIST)]
            cnt+=1
            host, port = _server.host, _server.port

        print(f"Forwarding request to backend localhost:{port}")

        backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_sock.connect((host, port))
        threading.Thread(target=pipe, args=(client_socket, backend_sock), daemon=True).start()
        threading.Thread(target=pipe, args=(backend_sock, client_socket), daemon=True).start()

        print("Response sent back to client")

    except Exception as e:
        print("Error:", e)

def run_proxy_server():
    pool = ThreadPoolExecutor(max_workers=4)
    lb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lb_sock.bind((PROXY_SERVER.get("host", "0.0.0.0"), int(PROXY_SERVER.get("port", 8000))))
    lb_sock.listen(128)

    print(f"Load balancer listening on port {PROXY_SERVER.get("port", 8000)}...")

    while True:
        client_socket, addr = lb_sock.accept()
        print(f"Request coming from {addr[0]}:{addr[1]}")
        pool.submit(forward_request_to_server, client_socket)


if __name__ == "__main__":
    run_proxy_server()