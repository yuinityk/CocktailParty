# -*- coding: utf-8 -*-

import socket
import pyaudio
import wave

WAVLEN = 768044 #This changes according to the RECORD_SECONDS, so you should change here in the future.


class Recorder():
    def __init__(self,addr,port):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # enable to access the same port continuously
        self.serverIP = addr
        self.port = port

    def rec(self,rate=44100,recsec=10,fname="rec.wav",idx=0):
        '''
        Record with the device of index number idx.
        '''
        p = pyaudio.PyAudio()
        # confirmation of index number
        count = p.get_device_count()
        devices = []
        for i in range(count):
            devices.append(p.get_device_info_by_index())
        for i, dev in enumerate(devices):
            print (i, dev['name'])
        p.terminate()

        FORMAT = pyaudio.paInt16
        CHANNELS = 1               # monoral
        RATE = rate                # sampling rate
        CHUNK = 2**11              # number of data point
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
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


class Client(Recorder):
    '''
    Receive an instruction to record from the server,
    record,
    and send data to the server.
    '''
    def __init__(self,addr = "localhost",port = 50007):
        super(Client,self).__init__(addr,port)

    def send(self,fname = "rec.wav"):
        f = open(fname, "rb")
        data = f.read()
        f.close()

        self.soc.bind((self.addr,self.port))
        self.soc.listen(1)
        soc, addr = self.soc.accept()
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
    and coordinate the two recordings.
    '''
    def __init__(self,addr = "localhost",port = 50007):
        super(Server,self).__init__(addr,port)

    def receive(self):
        self.soc.connect((self.serverIP, self.port))
        chunks = b''
        bytes_recd = 0
        while(1):
            chunk = self.soc.recv(min(WAVLEN-bytes_recd,2048))
            if chunk == "":
                self.soc.close()
                break
            chunks += chunk
            bytes_recd += len(chunk)

        f = open("received.wav","wb")
        f.write(chunks)
        f.close()

    def instruction(self):
        pass # to be developed

