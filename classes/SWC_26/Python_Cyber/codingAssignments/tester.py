<<<<<<< HEAD:NotesMD/classes/SWC_26/Python_Cyber/codingAssignments/tester.py
from socket import *
import time 
startTime = time.time()

# not sure what this means?
if __name__ == '__main__':
    print("<---------------Beginning of the Program------------------->")
    target = input('Enter the host you would like to be scanned: ')

    ip_address = gethostbyname(target)
    print ('Starting scan on host: ', ip_address)

# SCANNING PORTS IN THIS RANGE ON A SPECIFIC HOST 
    for i in range( 1, 443):
    
        # AF_NET --> indicates IPv4 address 
        # SOC_STREA --> indicates this is a TCP client ?
        socke = socket(AF_INET, SOCK_STREAM)

        # Trying to connect to each port  
        conn = socke.connect_ex((ip_address, i))

        # 0 indicates connected 
        if (conn == 0):
            print('Port %d: OPEN' % (i,))
            
        # what does it mean to open or close a socket? Open and close connection to IP?         
        socke.close()
    
print('Time taken:', time.time() - startTime)
print("Awesome, this is our first port scanner in python")
print("<--------------------Program Complete----------------> ")

''' Output is not as expected because of network config. Kali and Metasploitable have the
same IP addresses. Reason: both using NAT mode. 

'''
=======
from socket import *
import time 
startTime = time.time()

# not sure what this means?
if __name__ == '__main__':
    print("<---------------Beginning of the Program------------------->")
    target = input('Enter the host you would like to be scanned: ')

    ip_address = gethostbyname(target)
    print ('Starting scan on host: ', ip_address)

# SCANNING PORTS IN THIS RANGE ON A SPECIFIC HOST 
    for i in range( 1, 443):
    
        # AF_NET --> indicates IPv4 address 
        # SOC_STREA --> indicates this is a TCP client ?
        socke = socket(AF_INET, SOCK_STREAM)

        # Trying to connect to each port  
        conn = socke.connect_ex((ip_address, i))

        # 0 indicates connected 
        if (conn == 0):
            print('Port %d: OPEN' % (i,))
            
        # what does it mean to open or close a socket? Open and close connection to IP?         
        socke.close()
    
print('Time taken:', time.time() - startTime)
print("Awesome, this is our first port scanner in python")
print("<--------------------Program Complete----------------> ")

''' Output is not as expected because of network config. Kali and Metasploitable have the
same IP addresses. Reason: both using NAT mode. 

'''

>>>>>>> 2ad5c25 (Port Scanner Notes (Socket)):classes/SWC_26/Python_Cyber/codingAssignments/tester.py
