# -*- coding: utf-8 -*-

import socket
import pyaudio
import wave
import scipy.io.wavfile as wav
import parallel_record

WAVLEN = 860160 #This changes according to the RECORD_SECONDS, so you should change here in the future.
#860160 for recording for 10 seconds

serverIP = "10.213.197.163"
clientIP = "10.213.197.218"

class Recorder(object):
    def __init__(self,Addr_Server,Addr_Client,port):
        #self.soc_send    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.soc_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.soc_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # enable to access the same port continuously
        #self.soc_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverIP = Addr_Server
        self.clientIP = Addr_Client
        self.port = port

    def rec(self,rate=44100,recsec=3,fname="rec.wav",idx=5):
        '''
        Record with the device of index number idx.
        '''
        p = pyaudio.PyAudio()
        # confirmation of index number
        count = p.get_device_count()
        devices = []
        for i in range(count):
            devices.append(p.get_device_info_by_index(i))
        for i, dev in enumerate(devices):
            print (i, dev['name'])
        p.terminate()

        FORMAT = pyaudio.paInt16
        CHANNELS = 1               # monoral
        RATE = rate                # sampling rate
        CHUNK = 2**9              # number of data point
        RECORD_SECONDS = recsec
        WAVE_OUTPUT_FILENAME = fname

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            input_device_index=idx,
                            frames_per_buffer=CHUNK)
        print("recording...")

        frames = []
        for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK,exception_on_overflow=False)
            frames.append(data)
        print("finished recording")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(2)#audio.get_sample_size(FORMAT))
        #この変更が必要なのかは未検証
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))#[:WAVLEN])
        waveFile.close()


class Client(Recorder):
    '''
    Receive an instruction to record from the server,
    record,
    and send data to the server.
    '''
    def __init__(self,serv = serverIP,cli = clientIP,port = 50007):
        super(Client,self).__init__(serv,cli,port)

    def wait(self):
        self.soc_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc_receive.connect((self.serverIP, self.port))
        chunks = b''
        while(1):
            chunk = self.soc_receive.recv(2048)
            if chunk == "1":
                self.soc_receive.close() #ここでcloseして良いのかは未検証
                break
        self.rec()
        self.send()


    def send(self,fname = "rec.wav"):
        f = open(fname, "rb")
        data = f.read()
        f.close()

        self.soc_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc_send.bind((self.clientIP,self.port))
        self.soc_send.listen(10)
        soc, addr = self.soc_send.accept()
        print("Connected by" + str(addr))

        totalsent = 0
        while totalsent < len(data):
            sent = soc.send(data[totalsent:])
            totalsent += sent
        
        soc.send("") # the sign of the end
        soc.close()


class Server(Recorder):
    '''
    Send an instruction to record to the client,
    and at the same time record by itself.
    After that receive recorded data from the client
    and Adjust the two recording data.
    '''
    def __init__(self,serv=serverIP,cli=clientIP,port = 50007):
        super(Server,self).__init__(serv,cli,port)

    def receive(self):
        self.soc_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc_receive.connect((self.clientIP, self.port))
        chunks = b''
        bytes_recd = 0
        while(1):
            chunk = self.soc_receive.recv(min(WAVLEN-bytes_recd,2048))
            if chunk == "":
                self.soc_receive.close()
                break
            chunks += chunk
            bytes_recd += len(chunk)

        f = open("received.wav","wb")
        f.write(chunks)
        f.close()


    def instruction(self):
        self.soc_send    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # enable to access the same port continuously
        self.soc_send.bind((self.serverIP,self.port))
        self.soc_send.listen(10)
        soc, addr = self.soc_send.accept()
        print("Connected by" + str(addr))
        
        soc.send("1") # the sign of the end
        soc.close()
        self.soc_send.close()

    def postprocess(self):
        here = wav.read('rec.wav')[1]
        there = wav.read('received.wav')[1]
        everywhere = parallel_record.adjust(here,there)

        if everywhere == 0:
            pass
        elif everywhere > 0:
            here = here[everywhere:]
            there = there[:-everywhere]
        else:
            here = here[:everywhere]
            there = there[-everywhere:]
        
        wav.write('rec_here.wav',self.rate,here)
        wav.write('rec_there.wav',self.rate,there)


    def run(self):
        self.instruction()
        self.rec()
        self.receive()
        self.postprocess()
