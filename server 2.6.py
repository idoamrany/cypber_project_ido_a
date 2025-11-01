import socket
from datetime import datetime
import random
Queue_Len = 1
MAX_PACKET = 1024
SERVER_NAME = 'ido'
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(('0.0.0.0', 5000))
my_socket.listen(Queue_Len)


def rand():
    """
    הפונקצה מחזירה מספר רנדומלי בין 10 ל1
    """
    return random.randint(1,10)


def name():
    """
    הפונקציה מחזירה את השם של השרת
    """
    return SERVER_NAME


def main():
    while True:
        client_socket, address = my_socket.accept()
        try:
            while True:
                try:
                    request = client_socket.recv(MAX_PACKET).decode()
                    if request == 'TIME':
                        now = datetime.now()
                        readable_time = now.strftime("%H:%M:%S")
                        client_socket.send(readable_time.encode())
                    elif request == 'rand':
                        client_socket.send(str(rand()).encode())
                    elif request == 'name':
                        client_socket.send(name().encode())
                    elif request == 'exit':
                        client_socket.close()
                        break
                    else:
                        client_socket.send("Invalid request. Please try again".encode())
                except socket.error as error:
                    print("socket error om client socket"+ str(err))
        except socket.error as error:
            print("socket error on server socket"+ str(error))


if __name__ == '__main__':
    assert(name() == SERVER_NAME)
    assert(1 <= rand() <= 10)
    main()