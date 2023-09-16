import socket
import configs
from concurrent.futures import ThreadPoolExecutor,as_completed
from client_send import start
import sys



if __name__ =='__main__':
    with ThreadPoolExecutor() as pool:
        for ip in configs.server_list:
            people_name = sys.argv[1]
            if people_name=='E':
                order = 'END'
                pool.submit(start,order,ip,configs.PORT)
            action_name = sys.argv[2]

            file_name ='_'.join([people_name,action_name])
            print('file_name:'+file_name)
            pool.submit(start,file_name,ip,configs.PORT)














