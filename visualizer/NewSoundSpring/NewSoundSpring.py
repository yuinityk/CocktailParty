# -*- coding:utf-8 -*-
import numpy as np
import pyaudio
import pygame
from pygame.locals import *
import sys
import subprocess as sub

class MyAudioPlot:
    def __init__(self):
        self.CHUNK = 1024
        self.RATE = 44100#Hz
        self.audio = pyaudio.PyAudio()
        self.stream=self.audio.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.RATE,
                                    input=True,
                                    input_device_index=0,
                                    frames_per_buffer=self.CHUNK)

        #音声データの格納場所(プロットデータ)
        self.data=np.zeros(self.CHUNK*10)
        self.fft_data = self.FFT_AMP(self.data)
        self.fftfreq=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)
        self.y=self.fftfreq[1:len(self.fftfreq)/2]
        self.x=self.fft_data[1:len(self.fft_data)/2]
        self.plotdata = np.zeros([len(self.x),2])
       

    def update(self):
        self.data=np.append(self.data,self.AudioInput())
        if len(self.data)/1024 > 10:
            self.data=self.data[1024:]
            
    def fft(self):
        self.fft_data = self.FFT_AMP(self.data)
        self.fftfreq = np.fft.fftfreq(len(self.data), d=1.0/self.RATE)
        self.y=self.fftfreq[1:len(self.fftfreq)/2]
        self.x=self.fft_data[1:len(self.fft_data)/2]
        self.plotdata[:,0] = self.x
        self.plotdata[:,1] = self.y
        
	
    def set_spectrumdata(self):
    	np.savetxt('plotdata.csv',self.plotdata)

    def get_spectrum(self):
        self.threshold = 5
        spectrum = np.empty([0,2],float)
        count = 0
        for freq, amp in enumerate(self.x):
            if amp >= self.threshold:
                x = np.array([[self.y[freq],amp]])
                spectrum = np.append(spectrum,x,axis=0)
                count +=1
            if count > 300: break
        self.spectrum = spectrum
        return spectrum
        

    def AudioInput(self):
        ret=self.stream.read(self.CHUNK,exception_on_overflow=False)
        ret=np.frombuffer(ret, dtype="int16")/32768.0
        return ret

    def FFT_AMP(self, data):
        data=np.hamming(len(data))*data
        data=np.fft.fft(data)
        data=np.abs(data)
        return data

class MyGroup():
    def __init__(self,SCR_RECT):
        self.rect = SCR_RECT
        self.containers = np.empty([0,7],np.int32)

    def append(self, spectra):
        SCR_RECT = self.rect
        components = spectra.shape[0]
        new_data = np.zeros([components,7],dtype=np.int32)
        # x_coordinate
        new_data[:,0] = np.ones([1,components],dtype=np.int32)*SCR_RECT.midbottom[0]
        # y_coordinate
        new_data[:,1] = np.ones([1,components],dtype=np.int32)*SCR_RECT.midbottom[1]
        # vx
        new_data[:,2] = (np.random.randn(components)*5).astype(np.int32)
        # vy
        new_data[:,3] = -1*(self.amp2velocity(spectra[:,1])).astype(np.int32)
        # color
        new_data[:,4:7] = np.array(self.freq2color(spectra[:,0]), dtype=np.int32).T
        # append
        self.containers = np.append(self.containers,new_data,axis=0)
    
    def update(self):
        gravity =2.    #acceleration of gravity
        beta = 3.e-3 #viscous resistance coefficient
        alpha = 2.e-5   #inertial resistance coefficient
    
        #update x and y
        self.containers[:,0] = self.containers[:,0] + self.containers[:,2]
        self.containers[:,1] = self.containers[:,1] + self.containers[:,3]
        #update vx and vy
        self.containers[:,2] = self.containers[:,2] - (beta*self.containers[:,2]+alpha*self.containers[:,2]*self.containers[:,2]*np.sign(self.containers[:,2])).astype(np.int32)
        self.containers[:,3] = self.containers[:,3] + (gravity-beta*self.containers[:,3]-alpha*self.containers[:,3]*self.containers[:,3]*np.sign(self.containers[:,3])).astype(np.int32)
        SCR_RECT = self.rect
        bool = np.logical_or(np.logical_or(np.logical_or((self.containers[:,0]<SCR_RECT.left),(self.containers[:,0]>SCR_RECT.right)),(self.containers[:,1]>SCR_RECT.bottom)),(self.containers[:,1]<SCR_RECT.top-SCR_RECT.height*2))
        index = np.where(bool)
        self.containers = np.delete(self.containers,index,axis=0)

    def draw(self,screen):
        components = self.containers.shape[0]
        for i in range(components):
            x = self.containers[i,0]
            y = self.containers[i,1]
            color = (self.containers[i,4],self.containers[i,5],self.containers[i,6])
            pygame.draw.circle(screen, color, (x,y), 10)

    def amp2velocity(self, amp):
        gain = np.log2(amp)*7
        return (gain).astype(np.int32)

    def freq2color(self,freq):
        temperament = np.log2(freq/440.)*12
        temperament = temperament + 9 #真ん中のドを０に変更
        octave = np.floor(temperament/12.0)
        kind = temperament - 12.*octave
        
        hue = kind * 30
        lightness = np.where((40.+5.*octave > 0),40.+5.*octave,0)
        lightness = np.where(lightness < 100,lightness,100)
        
        bool = lightness < 50
        chroma = 100.-2.*(lightness-50.)*((-1)**bool)
        
        color = self.hsl2rgb(hue,chroma,lightness)
        return color


    def hsl2rgb(self,hue,chroma,lightness):
        
        if (lightness < 0).any() or (lightness > 100).any():
            print(u"the range of lightness is 0~100")
            sys.exit()
        elif (chroma < 0).any() or (chroma > 100).any():
            print(u"the range of chroma is 0~100")
            sys.exit()
        elif (lightness < chroma/2.).any() or (lightness > 100 - chroma/2.).any():
            print(u"the pair of chroma and lightness is invalid")
            sys.exit()
        
        elif (hue < 0).any() or (hue >= 360).any():
            print(u"Error: 0 <= hue < 360!!")
            sys.exit()

        max = 2.55*(lightness+chroma/2.)
        min = 2.55*(lightness-chroma/2.)

        data1 = min+(max-min)*(120-hue)/60.
        data2 = min+(max-min)*(hue-240)/60.
        case1 = np.logical_and(hue>=60,hue<120)
        case2 = np.logical_and(hue>=240,hue<300)
        case3 = np.logical_and(hue>=120,hue<240)
        
        red = np.where(case1,data1,np.where(case2,data2,np.where(case3,min,max)))

        data1 = min+(max-min)*hue/60.
        data2 = min+(max-min)*(240-hue)/60.
        case1 = np.logical_and(hue>=0,hue<60)
        case2 = np.logical_and(hue>=180,hue<240)
        case3 = np.logical_and(hue>=240,hue<360)
        
        green = np.where(case1,data1,np.where(case2,data2,np.where(case3,min,max)))
        
        data1 = min+(max-min)*(hue-120)/60.
        data2 = min+(max-min)*(360-hue)/60.
        case1 = np.logical_and(hue>=120,hue<180)
        case2 = np.logical_and(hue>=300,hue<360)
        case3 = np.logical_and(hue>=180,hue<300)
        
        blue = np.where(case1,data1,np.where(case2,data2,np.where(case3,max,min)))

        red = (red).astype(np.int32)
        green = (green).astype(np.int32)
        blue = (blue).astype(np.int32)

        return red, green, blue

SCR_RECT = Rect(0, 0, 800, 680)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    myaudioplot  = MyAudioPlot()
    group=MyGroup(SCR_RECT)
    clock = pygame.time.Clock()
    gnuplot = sub.Popen(["gnuplot"],stdin=sub.PIPE,)
    gnuplot.stdin.write("set size 1,1\n")
    gnuplot.stdin.write("set object 1 rect behind from screen 0,0 to screen 1,1 fc rgb \"#000000\" fillstyle solid 1.0\n")
    gnuplot.stdin.write("set border lc rgb \"white\"\n")
    gnuplot.stdin.write("set key tc rgb \"white\"\n")
    gnuplot.stdin.write("set xlabel \"xlabel\" tc rgb \"white\"\n")
    gnuplot.stdin.write("set ylabel \"ylabel\" tc rgb \"white\" offset 1, 0\n")
    gnuplot.stdin.write("unset key\n")
    gnuplot.stdin.write("set logscale x\n")
    gnuplot.stdin.write("set logscale y\n")
    gnuplot.stdin.write("set xlabel \"amplitude\"\n")
    gnuplot.stdin.write("set ylabel \"frequency\"\n")
    gnuplot.stdin.write("set xrange [1:100]\n")
    gnuplot.stdin.write("set yrange[10:22100]\n")
    while True:
        clock.tick(60)  # 60fps
        
        screen.fill((0,0,0))
        
        myaudioplot.update()
        myaudioplot.fft()
        myaudioplot.set_spectrumdata()
        gnuplot.stdin.write("plot \"plotdata.csv\" using 1:2 with lines lc rgb \"yellow\" \n")  
        
        spectrum = myaudioplot.get_spectrum()
        group.append(spectrum)
        group.draw(screen)
        group.update()
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                myaudioplot.stream.close()
                gnuplot.terminate()
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                myaudioplot.stream.close()
                gnuplot.terminate()
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()


