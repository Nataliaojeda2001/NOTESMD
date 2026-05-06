import socket 
import threading
''' 
allows for multi-thread program. In this case, 
allows for muliple clients and more than one request per client. 
'''

IP = '0.0.0.0'
PORT = 9998

# why a function called main?
def main():
    # creating a server object 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind = listen to this IP on this port 
    server.bind((IP, PORT))
    # 5 is a backlog, what does this mean and why is it needed?
    server.listen(5)
    '''
     python question: 
     
     print(f'{variable1} ... {variable2}')
     vs 
    print('hello, I am, %s my age %s)' % (variable1, variable2))
    '''
    print(f'[*] Listening on {IP}: {PORT}')
          
    # isn't this true all the time, is it because a server should be running cpntinously?
    while True:
        # receive a client socket object, receive the connection info in address variable
        client, address = server.accept()
        # when did we create a list to be able to do address[0] or is it because .accept returns a touple or a list? 
        print(f'Accepted a connection from {address[0]}: {address[1]}')
        # define client handler -> thread object 
        # why is a comma needed in args=(cleint, )) -> expecting 2 arguments?
        # from what im seeing, do we use the same client handler per connection? in other words we do not have a dedicated hadler per connection? cause in that case wouldnt we need a specific name for each one?
        client_handler = threading.Thread(target= handle_client, args=(client, ))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.rec(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.sent(b'ACK')

# I do not understand this 
if __name__ == '__main__':
    main()