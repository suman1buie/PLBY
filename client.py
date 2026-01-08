import os
import socket
from concurrent.futures import ThreadPoolExecutor

def send_request(req):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 8081))

    client_sock.sendall(req.encode())
    resp = client_sock.recv(2048)

    print(resp.decode())
    client_sock.close()

if __name__ == "__main__":
    print("Start sending all requests")
    pool = ThreadPoolExecutor(max_workers=4)
    for num in range(1, 10):
        message = f"sending request from {num}"
        pool.submit(send_request,message,)

    print("Done sending all requests")
