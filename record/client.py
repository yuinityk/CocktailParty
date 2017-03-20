# -*- coding: utf-8 -*-

import socket

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("localhost", 50007))
    
    while(1):
        data = soc.recv(1024)       #データ受信    
        
        if data == "q":             # qが押されたら終了
            soc.close()
            break
        receive = data
    
    f=open("jklm_new.txt","wb")     #ファイル書き込み
    f.write(receive)
    f.close()

if __name__ == '__main__':

    main()
