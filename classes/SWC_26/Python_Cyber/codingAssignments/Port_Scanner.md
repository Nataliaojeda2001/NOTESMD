# Python Scanner Notes 

Code was unable to run at first because they were not on an internal network. I changed the network settings for both VM's to internal network. Neither of them were assigned an IP address so then I had to manually assign them. 

I assigned Metasploit 192.168.56.11 and the Kali machine 192.168.56.10. 

## Commands ran in the terminal in Metasploitable VM:

no ip after running:
    
    ip a 
Manually assigning ip address:

    sudo ip link set eth0 up 
    sudo ip addr add 192.168.56.11/24 dev eth0

ip appears after running:
    
    ip a


## Commands ran in the terminal of Kali VM:

Network kept disconnecting in kali despite having it set to internal network so i had to stop the NetworkManager:

    sudo systemctl stop NetworkManager

commands to manually assign a IP address 
    
    sudo ip link set eth0 up 
    sudo ip addr add 192.168.56.10/24 dev eth0

check if kali knows any physical address but there was an empty output 

    arp -n 

Tried to ping metaspolitable VM: failed 

    ping 192.168.56.10 

## Commands ran in the terminal in Metasploitable VM:

Tried pinging kali: success

    ping 192.168.56.11

I learned since ping from kali -> metasploitable was not working and metasploitable -> kali was working, this may be a firewall issue on the metasploitable side. 

flush firewall 
    
    sudo iptables -F 

accept input: solved problem 

    sudo iptables -P INPUT ACCEPT 


## Commands ran in the terminal of Kali VM:

tried arp -n again: success 

    arp -n 

ping metasploitable: success 
    
    ping 192.168.56.11

# SCANNING METASPLOITABLE 


tester.py | scanning using socket  

```python
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

```

## *output*

```text
<---------------Beginning of the Program------------------->
Enter the host you would like to be scanned: 192.168.56.11
Starting scan on host:  192.168.56.11
Port 21: OPEN
Port 22: OPEN
Port 23: OPEN
Port 25: OPEN
Port 53: OPEN
Port 80: OPEN
Port 111: OPEN
Port 139: OPEN
Time taken: 7.378233909606934
Awesome, this is our first port scanner in python
<--------------------Program Complete----------------> 

```

____________________

n_scanner.py | NMAP scanner 

```python

    import nmap

    # This is a port scanner object? 
    nmapScanner = nmap.PortScanner()

    print("Welcome to the simple nmap automation tool")
    print("<#######################>")

    ip_addr = input("Please enter the IP address you want to scan: ")

    print("The IP you entered is: ", ip_addr)

    type(ip_addr)

    #calling nmapScanner object's method scan 
    nmapScanner.scan(ip_addr, "1-1024")
    print(nmapScanner.scaninfo())

    # where is this list updated? 
    for host in nmapScanner.all_hosts():
        print("--------------------------------")
        print('Host : %s (%s)' % (host, nmapScanner[ip_addr]))
        print( 'State : %s'% nmapScanner[ip_addr].state())

        for proto in nmapScanner[ip_addr].all_protocols():
            print("--------")
            print('Protocol : %s' % proto)

            targetport = nmapScanner[ip_addr][proto].keys()
            #lport.sort()
            for port in targetport:
                print('port : %s \tstate : %s'% (port, nmapScanner[ip_addr][proto]))      

```

## *output*

```text
Welcome to the simple nmap automation tool
<#######################>
Please enter the IP address you want to scan: 192.168.56.11
The IP you entered is:  192.168.56.11
{'tcp': {'method': 'syn', 'services': '1-1024'}}
--------------------------------
Host : 192.168.56.11 ({'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.56.11', 'mac': '08:00:27:91:CB:AA'}, 'vendor': {'08:00:27:91:CB:AA': 'Oracle VirtualBox virtual NIC'}, 'status': {'state': 'up', 'reason': 'arp-response'}, 'tcp': {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}})
State : up
--------
Protocol : tcp
port : 21       state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 22       state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 23       state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 25       state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 53       state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 80       state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 111      state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 139      state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 445      state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 512      state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 513      state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}
port : 514      state : {21: {'state': 'open', 'reason': 'syn-ack', 'name': 'ftp', 'product': 'vsftpd', 'version': '2.3.4', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:vsftpd:vsftpd:2.3.4'}, 22: {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh', 'product': 'OpenSSH', 'version': '4.7p1 Debian 8ubuntu1', 'extrainfo': 'protocol 2.0', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 23: {'state': 'open', 'reason': 'syn-ack', 'name': 'telnet', 'product': 'Linux telnetd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 25: {'state': 'open', 'reason': 'syn-ack', 'name': 'smtp', 'product': 'Postfix smtpd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:postfix:postfix'}, 53: {'state': 'open', 'reason': 'syn-ack', 'name': 'domain', 'product': 'ISC BIND', 'version': '9.4.2', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:isc:bind:9.4.2'}, 80: {'state': 'open', 'reason': 'syn-ack', 'name': 'http', 'product': 'Apache httpd', 'version': '2.2.8', 'extrainfo': '(Ubuntu) DAV/2', 'conf': '10', 'cpe': 'cpe:/a:apache:http_server:2.2.8'}, 111: {'state': 'open', 'reason': 'syn-ack', 'name': 'rpcbind', 'product': '', 'version': '2', 'extrainfo': 'RPC #100000', 'conf': '10', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: WORKGROUP', 'conf': '10', 'cpe': 'cpe:/a:samba:samba'}, 512: {'state': 'open', 'reason': 'syn-ack', 'name': 'exec', 'product': 'netkit-rsh rexecd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:linux:linux_kernel'}, 513: {'state': 'open', 'reason': 'syn-ack', 'name': 'login', 'product': '', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': ''}, 514: {'state': 'open', 'reason': 'syn-ack', 'name': 'shell', 'product': 'Netkit rshd', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:netkit:netkit_rsh'}}

```
