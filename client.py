import os
import socket
from concurrent.futures import ThreadPoolExecutor

def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8081))

    client_socket.sendall(request.encode())
    response = client_socket.recv(2048)

    print(response.decode())
    client_socket.close()

if __name__ == "__main__":
    print("Start sending all requests")
    pool = ThreadPoolExecutor(max_workers=4)
    for request_number in range(1, 10):
        message = f"sending request from {request_number}"
        pool.submit(send_request,message,)

    print("Done sending all requests")
