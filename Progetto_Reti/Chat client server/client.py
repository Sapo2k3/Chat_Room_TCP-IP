from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkt.END, msg)
        except OSError as e:
            print("Error while receiving message:", e)
            break

def send(event=None):
    try:
        msg = my_msg.get()
        my_msg.set("")
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            window.quit()
    except Exception as e:
        print("Error while sending message:", e)

def on_closing(event=None):
    try:
        my_msg.set("{quit}")
        send()
    except Exception as e:
        print("Error while closing the window:", e)

window = tkt.Tk()
window.title("Chat room")

messages_frame = tkt.Frame(window)
my_msg = tkt.StringVar()
my_msg.set("")
scrollbar = tkt.Scrollbar(messages_frame)

msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkt.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)

entry_field.pack()
send_button = tkt.Button(window, text="Send", command=send)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Enter the Server host: ')
PORT = input('Enter the server host port: ')
if not PORT:
    PORT = 40496
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkt.mainloop()
except Exception as e:
    print("Error while connecting to the server:", e)