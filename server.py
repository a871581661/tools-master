import socket
import configs
from record import start_record,end_record,check_record_file
from threading import Thread
global pid_list
global file_name

def socket_loop():
    global pid_list
    global file_name
    try:
        listenSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostName = socket.gethostname()
        listenSocket.bind((hostName,configs.PORT))
        listenSocket.listen(5)
        while True:
            dataSocker, addr = listenSocket.accept()
            while True:
                rec = dataSocker.recv(configs.BUFLEN)
                #给空bytes，表示对方关闭链接
                if not rec:
                    break
                info = rec.decode()
                print(f'order:{info}')
                if info == 'END':

                    if pid_list :
                        end_stat = end_record(pid_list)
                        if end_stat:
                            print('END_Finish')
                        else:
                            raise NameError('end fail')
                        isExist,fsize = check_record_file(file_name)
                        if isExist:
                            print(fsize)
                            dataSocker.send(f'success&fszie:{fsize}'.encode())
                        else:
                            dataSocker.send(b'fail')
                            raise NameError('recorder fail')
                    else:
                        dataSocker.send(b'pid_list_not_exit')
                        raise NameError('pid_list_not_exit,record fail')
                    break

                else:
                    file_name = info
                    pid_list = start_record(file_name)
                    dataSocker.send(b'start_record')
            dataSocker.close()
            listenSocket.close()
            break
    except KeyboardInterrupt:
        if dataSocker:
            dataSocker.close()
        if listenSocket:
            listenSocket.close()

if __name__ =='__main__':
    pid_list = []
    print('ip:',socket.gethostbyname(socket.gethostname()))
    while True:
        socket_loop()






