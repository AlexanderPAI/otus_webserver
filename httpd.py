import logging
import socket
import threading

logging.basicConfig(level=logging.DEBUG)


HOST = "localhost"
PORT = 8080
DOCUMENT_ROOT = "./www"  # root folder for static files


def handle_request(client_socket):
    try:
        # 1 get request
        request = client_socket.recv(1024).decode("utf-8")
        logging.info(f"Received request: {request}")

        # 2 get headers
        headers = request.split("\r\n")[0]

        # 3 split headers to methods
        method = headers.split(" ")[0]

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        if method == "GET":
            client_socket.send(response.encode("utf-8"))

    finally:
        client_socket.close()


def start_server():

    # 1. create sockets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. bind socket to address and port
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    # 3. in while loop create threads with function for handle_request
    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(
            target=handle_request, args=(client_socket,), daemon=True
        )
        client_handler.start()


if __name__ == "__main__":
    logging.info("Starting HTTP server")
    start_server()
