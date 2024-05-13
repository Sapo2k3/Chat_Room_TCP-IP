from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

close = False

def accept_incoming_connections():
    while True:
        try:
            client, client_address = SERVER.accept()
            print("%s:%s connected." % client_address)
            client.send(bytes("Hello! Type your Name followed by Enter!", "utf8"))
            addresses[client] = client_address
            Thread(target=handle_client, args=(client,)).start()
        except KeyboardInterrupt:
            break
        except Exception as e:
            if not close:
                print("Error accepting a connection:", e)
            break

def handle_client(client):  
    try:
        name = client.recv(BUFSIZ).decode("utf8")
        welcome = 'Welcome %s! If you want to leave the Chat, type {quit} to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
        
        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the Chat." % name, "utf8"))
                break
    except KeyboardInterrupt:
        print("\n")
    except Exception as e:
        print("Error handling a client connection:", e)

def broadcast(msg, prefix=""):  
    for user in clients:
        user.send(bytes(prefix, "utf8") + msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 8080
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    try:
        SERVER.listen(5)
        print("Waiting for connections...")
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except KeyboardInterrupt:
        print("Server interrupted.")
        close = True
        SERVER.close()
        exit()