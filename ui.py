import argparse
import platform
import shutil
import time
from numpy import random
import argparse
import os
import sys
from pathlib import Path
import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from detector import Detector
import time


def det_yolov5v6(info1):
    if info1[-3:] in ['jpg', 'png', 'jpeg', 'tif', 'bmp', 'JPG']:
        image = cv2.imread(info1)  # 读取识别对象
        try:
            bboxes = detector.detect(image)
            for i in bboxes:
                box = i[1]
                p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
                color = [0, 0, 255]
                ui.printf(str(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))) + '检测到' + str(i[0]))
                cv2.rectangle(image, p1, p2, color, thickness=3, lineType=cv2.LINE_AA)
                score = float(i[2])
                cv2.putText(image, str(i[0]) + ' ' + str(score)[:5], (int(box[0]), int(box[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        except:
            pass
        ui.showimg(image)
        QApplication.processEvents()

    if info1[-3:] in ['mp4', 'avi']:
        capture = cv2.VideoCapture(info1)
        fps = capture.get(cv2.CAP_PROP_FPS)  # 视频平均帧率
        while True:
            _, image = capture.read()
            if image is None:
                break
            try:
                bboxes = detector.detect(image)
                for i in bboxes:
                    box = i[1]
                    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
                    color = [0, 0, 255]
                    ui.printf(
                        str(time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))) + '检测到' + str(i[0]))
                    cv2.rectangle(image, p1, p2, color, thickness=3, lineType=cv2.LINE_AA)
                    score = float(i[2])
                    cv2.putText(image, str(i[0]) + ' ' + str(score)[:5], (int(box[0]), int(box[1]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            except:
                pass
            ui.showimg(image)
            QApplication.processEvents()
            time.sleep(1 / fps)  # 按原帧率播放


class Thread_1(QThread):  # 线程1
    def __init__(self, info1):
        super().__init__()
        self.info1 = info1
        self.run2(self.info1)

    def run2(self, info1):
        result = []
        result = det_yolov5v6(info1)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 960)
        MainWindow.setStyleSheet("background-image: url(\"./template/a.jpeg\")")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(168, 60, 551, 71))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("")
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet("font-size:50px;font-weight:bold;font-family:SimHei;background:rgba(255,255,255,0);")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 188, 751, 501))
        self.label_2.setStyleSheet("background:rgba(255,255,255,1);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(73, 746, 851, 174))
        self.textBrowser.setStyleSheet("background:rgba(0,0,0,0);")
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1020, 750, 150, 40))
        self.pushButton.setStyleSheet("background:rgba(53,142,255,1);border-radius:10px;padding:2px 4px;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1020, 810, 150, 40))
        self.pushButton_2.setStyleSheet("background:rgba(53,142,255,1);border-radius:10px;padding:2px 4px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1020, 870, 150, 40))
        self.pushButton_3.setStyleSheet("background:rgba(53,142,255,1);border-radius:10px;padding:2px 4px;")
        self.pushButton_3.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "鸟巢检测系统"))
        self.label.setText(_translate("MainWindow", "鸟巢检测系统"))
        self.label_2.setText(_translate("MainWindow", "请添加对象，注意路径不要存在中文"))
        self.pushButton.setText(_translate("MainWindow", "选择对象"))
        self.pushButton_2.setText(_translate("MainWindow", "开始识别"))
        self.pushButton_3.setText(_translate("MainWindow", "退出系统"))

        # 点击文本框绑定槽事件
        self.pushButton.clicked.connect(self.openfile)
        self.pushButton_2.clicked.connect(self.click_1)
        self.pushButton_3.clicked.connect(self.handleCalc3)

    def openfile(self):
        global sname, filepath
        fname = QFileDialog()
        fname.setAcceptMode(QFileDialog.AcceptOpen)
        fname, _ = fname.getOpenFileName()
        if fname == '':
            return
        filepath = os.path.normpath(fname)
        sname = filepath.split(os.sep)
        ui.printf("当前选择的文件路径是：%s" % filepath)
        try:
            show = cv2.imread(filepath)
            ui.showimg(show)
        except:
            ui.printf('错误！输入的图片路径包含中文，请修改后重试！')

    def handleCalc3(self):
        os._exit(0)

    def printf(self, text):
        self.textBrowser.append(text)
        self.cursor = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursor.End)
        QtWidgets.QApplication.processEvents()

    def showimg(self, img):
        global vid
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)
        n_width = _image.width()
        n_height = _image.height()
        if n_width / 500 >= n_height / 400:
            ratio = n_width / 800
        else:
            ratio = n_height / 800
        new_width = int(n_width / ratio)
        new_height = int(n_height / ratio)
        new_img = _image.scaled(new_width, new_height, Qt.KeepAspectRatio)
        self.label_2.setPixmap(QPixmap.fromImage(new_img))

    def click_1(self):
        global filepath
        try:
            self.thread_1.quit()
        except:
            pass
        self.thread_1 = Thread_1(filepath)  # 创建线程
        self.thread_1.wait()
        self.thread_1.start()  # 开始线程


if __name__ == "__main__":
    global detector
    detector = Detector()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
