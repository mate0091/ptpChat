import ssl
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        secure_socket = context.wrap_socket(client, server_side = True)
        print("%s:%s has connected." % client_address)
        secure_socket.send(bytes("Greetings! Type your name and press enter", "utf8"))
        addresses[secure_socket] = client_address
        Thread(target=handle_client, args=(secure_socket,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}
secure_socket = 0;

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile="server.crt", keyfile="server.key")
context.load_verify_locations(cafile="client.crt")

SERVER = socket(AF_INET, SOCK_STREAM)

if __name__ == "__main__":
    SERVER.bind(ADDR)
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    secure_socket.close()