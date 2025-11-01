import  socket
MAX_PACKET = 1024
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    my_socket.connect(("127.0.0.1", 5000))
    while True:
        request = input('enter your request (use four letters) \n ')
        while len (request) != 4:
            print ("the request is too long")
            request = input('enter your request (use four letters) \n ')
        my_socket.send(request.encode())
        response = my_socket.recv(MAX_PACKET).decode()
        print(response)
        if response == "exit":
            break
except socket.error as error:
    print ("received error:" + str(error))
