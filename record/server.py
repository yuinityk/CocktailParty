# -*- coding: utf-8 -*-

import socket

def main():

    f=open("rec.wav","rb")        #録音ファイルを開く
    data=f.read()
    f.close()
    
    print(len(data))        #データサイズ
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 50007))    # 指定したホスト(IP)とポートをソケットに設定
    s.listen(1)                     # 1つの接続要求を待つ
    soc, addr = s.accept()          # 要求が来るまでブロック
    print("Conneted by"+str(addr))  #サーバ側の合図

    totalsent = 0
    while totalsent < len(data):
        sent = soc.send(data[totalsent:])
        totalsent += sent
    soc.send("")
    soc.close()

if __name__ == '__main__':

    main()
