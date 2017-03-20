# -*- coding: utf-8 -*-

import socket

def main():

    f=open("jklm.txt","rb")        #録音ファイルを開く
    data=f.read(1)
    f.close()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 50007))    # 指定したホスト(IP)とポートをソケットに設定
    s.listen(1)                     # 1つの接続要求を待つ
    soc, addr = s.accept()          # 要求が来るまでブロック
    print("Conneted by"+str(addr))  #サーバ側の合図

    soc.send(data)              # ソケットにデータを送信
    soc.send("q")
    soc.close()

if __name__ == '__main__':

    main()
