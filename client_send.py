import socket
import configs


def start(order:str,ip,port):
    cilentSocket = creat_connect(ip,port)
    send(cilentSocket,order)
    recv(cilentSocket)



def creat_connect(ip,port):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ip, port))
    return clientSocket

def send(socket:socket.socket,file_name:str):
    data = file_name.encode()
    socket.send(data)

def recv(socket:socket.socket):
    recv_data = socket.recv(1024)
    data = recv_data.decode('GBK')
    serverip = socket.getpeername()
    print(serverip,data)







