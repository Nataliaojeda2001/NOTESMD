import socket


target_host = "google.com"
target_port = 80 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect requires a tuple (x,y) that includes the ip, port 
client.connect((target_host, target_port))

# b stands for bytes?
# how do we know what the format is and the headers 
client.send(b'GET /HTTP/1.1\r\nHost: google.com\r\n\r\n')

# number is how many bites to receive 
# what decides the options for the number of bites to recieve and what are the options and why 
response = client.recv(4096)

print(response.decode())

client.close()