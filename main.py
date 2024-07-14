import socket
import os
import mimetypes
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
import pymongo

# Налаштування бази даних MongoDB
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client["messages_db"]
collection = db["messages"]

# HTTP-сервер
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/templates/index.html'
        elif self.path == '/message.html':
            self.path = '/templates/message.html'
        elif self.path == '/messages':
            self.handle_get_messages()
            return
        elif self.path.startswith('/static/'):
            self.path = self.path[1:]  # Видаляємо провідний слеш

        if os.path.exists(self.path[1:]):
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(self.path[1:])
            if mime_type:
                self.send_header('Content-type', mime_type)
            self.end_headers()
            with open(self.path[1:], 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/error.html', 'rb') as file:
                self.wfile.write(file.read())

    def handle_get_messages(self):
        messages = list(collection.find({}, {"_id": 0}).sort("date", -1))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(messages).encode('utf-8'))

    def do_POST(self):
        if self.path == '/send':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            message = json.loads(post_data)

            # Відправка даних на Socket-сервер
            send_to_socket_server(message)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Message received and sent to socket server")

def send_to_socket_server(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5001))
    client_socket.sendall(json.dumps(message).encode('utf-8'))
    client_socket.close()

def run_http_server():
    httpd = HTTPServer(('0.0.0.0', 3000), SimpleHTTPRequestHandler)
    print("HTTP Server running on port 3000")
    httpd.serve_forever()

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    message = json.loads(request.decode('utf-8'))
    message["date"] = datetime.now().isoformat()
    collection.insert_one(message)
    print(f"Message saved: {message}")
    client_socket.close()

def run_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5001))
    server.listen(5)
    print("Socket Server running on port 5001")

    while True:
        client_sock, addr = server.accept()
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

if __name__ == "__main__":
    http_thread = threading.Thread(target=run_http_server)
    socket_thread = threading.Thread(target=run_socket_server)

    http_thread.start()
    socket_thread.start()

    http_thread.join()
    socket_thread.join()
