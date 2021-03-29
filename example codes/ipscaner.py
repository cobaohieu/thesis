import subprocess 
  
for ping in range(1,10): 
    address = "127.0.0." + str(ping) 
    res = subprocess.call(['ping', '-c', '3', address]) 
    if res == 0: 
        print( "ping to", address, "OK") 
    elif res == 2: 
        print("no response from", address) 
    else: 
        print("ping to", address, "failed!") 
# import socket 
  
# #creates a new socket using the given address family. 
# socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
# #setting up the default timeout in seconds for new socket object 
# socket.setdefaulttimeout(1) 
  
# #returns 0 if connection succeeds else raises error 
# result = socket_obj.connect_ex((addr,port)) #address and port in the tuple format 
  
# #closes te object 
# socket_obj.close() 