from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

# to recv message and decode
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFFSIZE).decode("utf8")
            if msg == "full":
                client_socket.close()
                top.quit()
                print("Sorry chat room full")
            else:
                msg_list.insert(tkinter.END, msg + '\n')
        except OSError:  # Possibly client has left the chat.
            break


# send message by encoding in utf8 and if client types exit, will close window
def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))


def on_closing(event=None):
    client_socket.send(bytes("exit", "utf8"))
    client_socket.close()
    top.quit()



#---------------------------------------------------------------------------------------------------------

print("Client Server...")
# client will have to enter host IP and port first before proceeding on GUI
listeningPort = input("Enter chat server's IP address and port: ")
list = listeningPort.split()
HOST = list[0]
PORT = int(list[1])
#HOST = input('Enter server IP: ')
#PORT = input('Enter port: ')
#if not PORT:
#    PORT = 1234
#else:
#    PORT = int(PORT)

BUFFSIZE = 1024
address = (HOST, PORT)

username = input("Enter Client's name: ")

print("Trying to connect to the server: %s, (%s)" %address)

top = tkinter.Tk()
top.title("CSC1010 Computer Network Assignment 2 Chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)
# set size of window
msg_list = tkinter.Listbox(messages_frame, height=15, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
top.configure(background='#808080')

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)
print("Connected...")

client_socket.send(bytes(username, "utf8"))
## using tkinter for GUI interface as gui has looping eventhandler that is able to load messages for groupchats ##

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()


