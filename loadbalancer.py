from concurrent.futures import ThreadPoolExecutor
import socket

SERVER_LIST = [8070, 8077, 8088]


def forward_request_to_server(client_socket, cnt):
    try:
        req = client_socket.recv(2048)

        port = SERVER_LIST[cnt % len(SERVER_LIST)]
        print(f"Forwarding request to backend localhost:{port}")

        backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_sock.connect(("127.0.0.1", port))

        backend_sock.sendall(req)
        resp = backend_sock.recv(2048)

        backend_sock.close()

        client_socket.sendall(resp)
        print("Response sent back to client")

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    pool = ThreadPoolExecutor(max_workers=4)
    lb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lb_sock.bind(("0.0.0.0", 8081))
    lb_sock.listen(128)

    print("Load balancer listening on port 8081...")

    cnt = 0
    while True:
        client_socket, addr = lb_sock.accept()
        print(f"Request coming from {addr[0]}:{addr[1]}")
        pool.submit(forward_request_to_server, client_socket, cnt)
        cnt += 1
