from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QBrush, QPainter, QKeySequence, QPixmap
from random import randint
import sys
from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave

class UpBox(QWidget):
    def __init__(self, parent=None):
        super(UpBox, self).__init__(parent)
        self.color = [randint(0,255), randint(0,255), randint(0,255)]
        self.changeBy = [-7, 5, 12]
        self.frameDelayMillis = self.catch()
        self.timerID = self.startTimer(self.frameDelayMillis)


    def paintEvent(self, event):
        qp = QPainter(self)
        rect = self.rect()
        color = QColor(self.color[0], self.color[1], self.color[2])
        brush = QBrush(color, Qt.SolidPattern)
        qp.setBrush(brush)
        qp.setPen(Qt.NoPen)
        qp.drawRect(rect)

    def timerEvent(self, event):
        self.updateColor()
        self.update()

    def updateColor(self):
        for i in [0,1,2]:
            self.color[i] = self.color[i] + self.changeBy[i]
            if self.color[i] < 0:
                self.color[i] = 0
                self.changeBy[i] *= -1 # reverse direction
            elif self.color[i] > 255:
                self.color[i] = 255
                self.changeBy[i] *= -1 # reverse direction

    def catch(self, sindex):
        i = 0

        if i < 1000:
            def catchsound(self):
                NUM_SAMPLES = 2000
                SAMPLING_RATE = 8000
                COUNT_NUM = 20
                SAVE_LENGTH = 8

                pa = PyAudio()
                stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
                                frames_per_buffer=NUM_SAMPLES)
                save_count = 0
                save_buffer = []

                while True:

                    string_audio_data = stream.read(NUM_SAMPLES)
                    audio_data = np.fromstring(string_audio_data, dtype=np.short)
                    large_sample_count = np.sum( audio_data > LEVEL )
                    sindex = int(npmax(audio_data))
                    print(sindex)

                    if sindex < 1000:
                        sindex = 0
                    else:
                        continue


    def setSpeed(self, frameDelay):
        self.killTimer(self.timerID)
        self.frameDelayMillis = frameDelay
        self.timerID = self.startTimer(self.frameDelayMillis)


class MyWin(QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.initGUI()

    def initGUI(self):
        mainLayout = QVBoxLayout()
        centerWidget = QWidget()
        centerWidget.setObjectName("parent")
        centerWidget.setLayout(mainLayout)
        self.setCentralWidget(centerWidget)
        self.setWindowTitle("Load Styles from a .css File")
        self.setFixedWidth(360)
        self.setFixedHeight(480)
        self.box = UpBox(self)
        self.box.resize(360,50)

        txt = QLabel("WeChat")
        head = QHBoxLayout()
        head.addWidget(txt)
        headbox = QGroupBox()
        headbox.setObjectName("headbox")
        headbox.setLayout(head)
        mainLayout.addWidget(headbox)

        body = QFormLayout()
        pix = QLabel()
        pix.setPixmap(QPixmap("success.png"))
        body.addWidget(pix)
        picBox = QGroupBox()
        picBox.setObjectName("formbox")
        picBox.setLayout(body)
        mainLayout.addWidget(picBox)

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MyWin()
    win.show()
    sys.exit(app.exec_())
