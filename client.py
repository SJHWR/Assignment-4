import socket
import threading


#The purpose of this function is to receive the message sent by the client and print it out
def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break
#Let the user choose the option to send a message
def send_messages(client):
    while True:
        option = input("Choose an option - 1: Send to everyone, 2: Private message, 3: Disconnect: ")
        if option == '1':
            message = input("Enter your message: ")
            client.sendall(f'MSG:{message}'.encode('utf-8'))
        elif option == '2':
            target_nickname = input("Enter the nickname of the person: ")
            message = input("Enter your message: ")
            client.sendall(f'PMSG:{target_nickname}:{message}'.encode('utf-8'))
        elif option == '3':
            client.sendall('DISCONNECT'.encode('utf-8'))
            client.close()
            break
        else:
            print("Invalid option. Please try again.")

def main():
    nickname = input("Choose your nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 55555))

    client.sendall(f'NICK:{nickname}'.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    send_messages(client)

if __name__ == '__main__':
    main()
