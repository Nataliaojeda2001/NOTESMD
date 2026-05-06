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
print(nmapScanner.scanifo())

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
          