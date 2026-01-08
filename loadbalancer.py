from concurrent.futures import ThreadPoolExecutor
import socket
import threading

lock = threading.Lock()

SERVER_LIST = [8070, 8077, 8088]
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
            port = SERVER_LIST[cnt % len(SERVER_LIST)]
            cnt+=1
        
        print(f"Forwarding request to backend localhost:{port}")

        backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_sock.connect(("127.0.0.1", port))
        threading.Thread(target=pipe, args=(client_socket, backend_sock), daemon=True).start()
        threading.Thread(target=pipe, args=(backend_sock, client_socket), daemon=True).start()

        print("Response sent back to client")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    pool = ThreadPoolExecutor(max_workers=4)
    lb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lb_sock.bind(("0.0.0.0", 8081))
    lb_sock.listen(128)

    print("Load balancer listening on port 8081...")

    while True:
        client_socket, addr = lb_sock.accept()
        print(f"Request coming from {addr[0]}:{addr[1]}")
        pool.submit(forward_request_to_server, client_socket)
