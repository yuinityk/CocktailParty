# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import numpy as np
import scipy.io.wavfile as wav
from sklearn.decomposition import FastICA
import os.path
import random
import time
import pyaudio
import wave


RATE =  44100
max_input = 10


class menu_widget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(menu_widget, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.set_button = QtGui.QPushButton('楽曲セット',self)
        self.sep_button = QtGui.QPushButton('分離・復元',self)
        self.label1 = QtGui.QLabel('曲数',self)
        self.combobox = QtGui.QComboBox(self)
        for i in range(max_input-1):
            self.combobox.addItem(str(i+2))
        self.label2 = QtGui.QLabel('ジャンル',self)
        self.albumcombobox = QtGui.QComboBox(self)
        self.albumcombobox.addItem("J-POP")
        self.albumcombobox.addItem("童謡")
        self.albumcombobox.addItem("アニソン")
        
        font = QtGui.QFont()
        font.setPointSize(15)
        self.set_button.setFont(font)
        self.sep_button.setFont(font)
        self.label1.setFont(font)
        self.combobox.setFont(font)
        self.label2.setFont(font)
        self.albumcombobox.setFont(font)

        
        self.subhbox1 = QtGui.QHBoxLayout()
        self.subhbox1.addWidget(self.label1,alignment=QtCore.Qt.AlignRight)
        self.subhbox1.addWidget(self.combobox)

        self.subhbox2 = QtGui.QHBoxLayout()
        self.subhbox2.addWidget(self.label2,alignment=QtCore.Qt.AlignRight)
        self.subhbox2.addWidget(self.albumcombobox)
        
        self.hbox = QtGui.QHBoxLayout(self)
        self.hbox.addWidget(self.set_button)
        self.hbox.addWidget(self.sep_button)
        self.hbox.addLayout(self.subhbox1)
        self.hbox.addLayout(self.subhbox2)
        self.setLayout(self.hbox)

    def get_combo_value(self):
        value = self.combobox.currentIndex()+2
        return value

    def get_album_name(self):
        value = self.albumcombobox.currentIndex()+1
        return "album"+str(value)


class music_widget(QtGui.QWidget):
    def __init__(self, parent=None, label_name=None, filename=None):
        super(music_widget, self).__init__(parent)
        self.initUI(label_name,filename)
    
    def initUI(self, label_name, filename):
        if label_name is None:
            self.label_name = "NoName"
        else:
            self.label_name = label_name
        self.label = QtGui.QLabel(self.label_name,self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        
        self.button = QtGui.QPushButton('再生',self)
        self.filename = filename
        
        self.hbox = QtGui.QHBoxLayout(self)
        self.hbox.addWidget(self.label,stretch=3)
        self.hbox.addWidget(self.button,stretch=1)
        self.setLayout(self.hbox)
        
    clickedme = QtCore.pyqtSignal(str)

    def press_buttom(self):
        self.clickedme.emit(self.filename)


class Walker(QtCore.QThread):

    def __init__(self, parent=None):
        super(Walker, self).__init__(parent)
        self.filename = ""
        self.stopped = False
        self.mutex = QtCore.QMutex()

    def setup(self, filename):
        self.filename = filename
        self.stopped = False

    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True
    
    def run(self):
        CHUNK = 1024
        filename = self.filename
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(CHUNK)

        while data != '':
            if self.stopped:
                return
            stream.write(data)
            data = wf.readframes(CHUNK)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        self.stop()
        self.finished.emit()


class _mixed_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(_mixed_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components
        
        self.vbox = QtGui.QVBoxLayout(self)
        self.music = [music_widget(parent=self,label_name="Mix"+str(i+1),filename="mixed/mixed"+str(i+1)+".wav") for i in range(self.n_components)]
        for i in range(self.n_components):
            self.vbox.addWidget(self.music[i])
        self.setLayout(self.vbox)

class mixed_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(mixed_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components

        self.label = QtGui.QLabel("混合音源",self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self._mixed = _mixed_widget(self,self.n_components)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.label,stretch=1)
        self.vbox.addWidget(self._mixed,stretch=10)
        self.setLayout(self.vbox)


class _sep_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(_sep_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components
        
        self.vbox = QtGui.QVBoxLayout(self)
        self.music = [music_widget(parent=self,label_name="Separated"+str(i+1),filename="separated/separated"+str(i+1)+".wav") for i in range(components)]
        for i in range(components):
            self.vbox.addWidget(self.music[i])
        self.setLayout(self.vbox)

class sep_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(sep_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components
        
        self.label = QtGui.QLabel("分離・復元音源",self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        self._sep = _sep_widget(self,self.n_components)
        
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.label,stretch=1)
        self.vbox.addWidget(self._sep,stretch=10)
        self.setLayout(self.vbox)

class _title_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(_title_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components
        
        self.vbox = QtGui.QVBoxLayout(self)
        self.label = [QtGui.QLabel("No Title",self) for i in range(components)]
        font = QtGui.QFont()
        font.setPointSize(20)
        for i in range(components):
            self.label[i].setFont(font)
            self.vbox.addWidget(self.label[i],alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.vbox)

class title_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(title_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components
    
        self.label = QtGui.QLabel("タイトル名",self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        self._title = _title_widget(self,self.n_components)
    
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.label,stretch=1)
        self.vbox.addWidget(self._title,stretch=10)
        self.setLayout(self.vbox)

class _rate_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(_rate_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components
        
        self.vbox = QtGui.QVBoxLayout(self)
        self.label = [QtGui.QLabel("0.0 %",self) for i in range(components)]
        font = QtGui.QFont()
        font.setPointSize(20)
        for i in range(components):
            self.label[i].setFont(font)
            self.vbox.addWidget(self.label[i])
        self.setLayout(self.vbox)

class rate_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(rate_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components
        
        self.label = QtGui.QLabel("復元率",self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        self._rate = _rate_widget(self,self.n_components)
        
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.label,stretch=1)
        self.vbox.addWidget(self._rate,stretch=10)
        self.setLayout(self.vbox)

class main_widget(QtGui.QWidget):
    def __init__(self, parent=None, components=None):
        super(main_widget, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self, components):
        if components is None:
            self.n_components = 2
        elif components < 2:
            print u"Error!"
            sys.exit()
        else:
            self.n_components = components
        
        self.mixed = mixed_widget(self,self.n_components)
        self.sep = sep_widget(self,self.n_components)
        self.title = title_widget(self,self.n_components)
        self.rate = rate_widget(self,self.n_components)
        
        self.hbox = QtGui.QHBoxLayout(self)
        self.hbox.addWidget(self.mixed,stretch=2)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.sep,stretch=2)
        self.hbox.addWidget(self.title,stretch=4)
        self.hbox.addWidget(self.rate,stretch=1)
        self.setLayout(self.hbox)

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None, components=2):
        super(MainWindow, self).__init__(parent)
        self.initUI(components)
    
    def initUI(self,components):
        self.setWindowTitle("Music Quiz")
        self.titlelabel=QtGui.QLabel('<h1>〜曲当てクイズ〜</h1>',self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.titlelabel.setFont(font)
        self.menu = menu_widget(self)
        self.n_components = components
        self.main = main_widget(self,self.n_components)
        
        self.vbox = QtGui.QVBoxLayout(self)
        self.vbox.addWidget(self.titlelabel,stretch=1,alignment=QtCore.Qt.AlignCenter)
        self.vbox.addWidget(self.menu,stretch=1)
        self.vbox.addWidget(self.main,stretch=15)
        self.setLayout(self.vbox)
        
        self.desktop = QtGui.qApp.desktop()
        self.windowstate = False
        
        self.resize(self.desktop.width()*4/5,self.desktop.height()*4/5)
        self.menu.set_button.clicked.connect(self.set)
        self.menu.sep_button.clicked.connect(self.separate)
        self.walker = Walker(self)
        self.show()

    def keyPressEvent(self, hoge):
        if hoge.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif hoge.key() == QtCore.Qt.Key_F2:
            if self.windowstate:
                self.windowstate = False
                self.showNormal()
            else:
                self.windowstate = True
                self.showFullScreen()

    def play(self,filename):
        self.walker.stop()
        self.walker.wait()
        self.walker.setup(str(filename))
        self.walker.start()
    
    def set(self):
        self.walker.stop()
        self.walker.wait()
        self.n_components = self.menu.get_combo_value()
        self.main.close()
        self.main = main_widget(self,self.n_components)
        self.albumname = self.menu.get_album_name()
        if self.albumname == "album1":
            self.n_input = 13
        elif self.albumname == "album2":
            self.n_input = 18
        elif self.albumname == "album3":
            self.n_input = 10
        self.data_length=np.min([os.path.getsize(self.albumname+"/input"+str(i+1)+".wav") for i in range(self.n_input)])/2-44
        
        #input voice data
        index = random.sample(range(self.n_input),self.n_components)
        filenames = [(self.albumname+'/input' + str(i+1) + '.wav') for i in index]
        input=[(wav.read(filenames[i])[1][0:self.data_length]) for i in range(self.n_components)]
        S = np.array(input).T
        S = S*1.0/np.max(np.abs(S),axis=0)
        
        A=np.ones([self.n_components,self.n_components])-1.9*np.diag(np.ones(self.n_components))
        S=np.dot(S,A.T)
        
        #volume up = normalization
        S = S/np.max(np.abs(S))*32767
        S = S.astype(np.int16)
        
        filenames = [('mixed/mixed' + str(i+1) + '.wav') for i in range(self.n_components)]
        for i in range(self.n_components):
            wav.write(filenames[i],RATE,S[:,i])
            music = self.main.mixed._mixed.music[i]
            music.button.clicked.connect(music.press_buttom)
            music.clickedme.connect(self.play)

        self.vbox.addWidget(self.main,stretch=10)

    def separate(self):
        self.walker.stop()
        self.walker.wait()
        #input voice data
        filenames = [('mixed/mixed' + str(i+1) + '.wav') for i in range(self.n_components)]
        mixed=[(wav.read(filenames[i])[1][0:self.data_length]) for i in range(self.n_components)]
        S = np.array(mixed).T

        ica = FastICA(n_components=self.n_components)
        S_ = ica.fit_transform(S)


        #volume up = normalization
        S_ = S_/np.max(np.abs(S_))*32767
        S_ = S_.astype(np.int16)


        filenames = [('separated/separated' + str(i+1) + '.wav') for i in range(self.n_components)]
        for i in range(self.n_components):
            wav.write(filenames[i],RATE,S_[:,i])

        #input music title
        if self.albumname == "album1":
            titlename = ["前前前世／RADWIMPS",
                         "三日月／絢香",
                         "I believe／絢香",
                         "地上の星／中島みゆき",
                         "ultra soul／B'z",
                         "タマシイレボリューション／Superfly",
                         "Butterfly／木村カエラ",
                         "栄光の架け橋／ゆず",
                         "LaLaLa Love Song／久保田利伸",
                         "さくら（独唱）／森山直太朗",
                         "レーザービーム／Perfume",
                         "蕾／コブクロ",
                         "青いイナズマ／SMAP"]
        
        elif self.albumname == "album2":
            titlename = ["アイアイ",
                         "いぬのおまわりさん",
                         "うみ",
                         "かえるのうた",
                         "キラキラぼし",
                         "げんこつやまのたぬきさん",
                         "しゃぼん玉",
                         "ぞうさん",
                         "チューリップ",
                         "ちょうちょう",
                         "とんぼのめがね",
                         "めだかの学校",
                         "メリーさんのひつじ",
                         "もりのくまさん",
                         "やぎさんゆうびん",
                         "夕やけ小やけ",
                         "大きな栗の木の下で",
                         "赤とんぼ"]
        
        elif self.albumname == "album3":
            titlename = ["One Light／kalafina",
                         "不安定な神様／Suara",
                         "シュガーソングとビターステップ／UNISON SQUARE GARDEN",
                         "星灯／Suara",
                         "Rising Hope／Lisa",
                         "恋する図形／上坂すみれ",
                         "残酷な天使のテーゼ／高橋洋子",
                         "Shangri-La／angela",
                         "fantastic dreamer／Machico",
                         "飛竜の騎士／TRUE"]
        #input music data
        filenames = [(self.albumname+'/input' + str(i+1) + '.wav') for i in range(self.n_input)]
        input=[(wav.read(filenames[i])[1][0:self.data_length]) for i in range(self.n_input)]
        input = np.array(input)

        #output music data
        filenames = [('separated/separated' + str(i+1) + '.wav') for i in range(self.n_components)]
        output=[(wav.read(filenames[i])[1][0:self.data_length]) for i in range(self.n_components)]
        output = np.array(output)

        X = np.concatenate((input,output),axis=0)

        coef = np.abs(np.corrcoef(X)[self.n_input:self.n_input+self.n_components,0:self.n_input])

        #coef
        percent = np.max(coef,axis=1)*100.0
        index = np.argmax(coef,axis=1)

        for i in range(self.n_components):
            music = self.main.sep._sep.music[i]
            music.hbox.removeWidget(music.button)
            music.button.clicked.connect(music.press_buttom)
            music.clickedme.connect(self.play)
            music.hbox.addWidget(music.button,stretch=1)

            title = self.main.title._title
            title.vbox.removeWidget(title.label[i])
            title.label[i].close()
            title.label[i] = QtGui.QLabel(titlename[index[i]])
            font = QtGui.QFont()
            font.setPointSize(20)
            title.label[i].setFont(font)
            title.vbox.addWidget(title.label[i],alignment=QtCore.Qt.AlignCenter)
                
            rate = self.main.rate._rate
            rate.vbox.removeWidget(rate.label[i])
            rate.label[i].close()
            rate.label[i] = QtGui.QLabel(str(percent[i])[0:5]+" %")
            font = QtGui.QFont()
            font.setPointSize(20)
            rate.label[i].setFont(font)
            rate.vbox.addWidget(rate.label[i])


def main():
    app = QtGui.QApplication(sys.argv)
    QtCore.QTextCodec.setCodecForCStrings( QtCore.QTextCodec.codecForLocale() )
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

