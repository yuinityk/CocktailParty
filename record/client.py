# -*- coding: utf-8 -*-

import socket

WAVLEN = 768044

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("localhost", 50007))
    
    chunks = b""
    bytes_recd = 0
    while(1):
        chunk = soc.recv(min(WAVLEN-bytes_recd,2048))       #データ受信    
        
        if chunk == "":             # qが押されたら終了
            soc.close()
            break
        
        chunks += chunk
        bytes_recd += len(chunk)
    
    f=open("dl.wav","wb")     #ファイル書き込み
    f.write(chunks)
    f.close()

if __name__ == '__main__':

    main()
