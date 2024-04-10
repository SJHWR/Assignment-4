import socket
import threading

clients = []
nicknames = []

#Send a message to all customers
def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

#Private message to a customer
def private_message(nickname, message):
    if nickname in nicknames:
        index = nicknames.index(nickname)
        client = clients[index]
        client.send(f"Private message: {message}".encode('utf-8'))
#Receive the message sent by the client and perform the corresponding operation according to the content of the message
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('NICK:'):
                nickname = message.split(':')[1]
                nicknames.append(nickname)
                clients.append(client)
                print(f'Nickname of the client is {nickname}')
                broadcast(f'{nickname} joined the chat!')
            elif message.startswith('MSG:'):
                text = message.split(':', 1)[1]
                broadcast(text)
            elif message.startswith('PMSG:'):
                _, target_nickname, text = message.split(':', 2)
                private_message(target_nickname, text)
            elif message == 'DISCONNECT':
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames.pop(index)
                broadcast(f'{nickname} left the chat!')
                client.close()
                break
        except:
            continue
#This function is used to receive client connections
def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 55555))
    server.listen()
    print("Server is listening...")

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == '__main__':
    receive()
