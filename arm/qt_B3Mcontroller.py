#!/usr/bin/python3
# -*- coding: utf-8 -*-

import b3mCtrl
import time
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox, QMainWindow, QApplication)


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.pos = [0] * 10
        self.id = 1

        self.aaa = b3mCtrl.B3mClass()
        self.aaa.begin("/dev/ttyUSB0",1500000)
       
        print (self.aaa.setTrajectoryType(255,"EVEN"))
        print (self.aaa.setMode(255,"POSITION"))

        # self.showMaximized() 

    def initUI(self):      

        btn1_add = QPushButton("+", self)
        btn1_add.move(140, 20)
        
        btn1_sub = QPushButton("-", self)
        btn1_sub.move(140, 60)

        free_btn =QPushButton("FREE_MODE", self)
        free_btn.move(140, 100)

        close_btn =QPushButton("close", self)
        close_btn.move(140, 140)
        
        home_btn =QPushButton("HOME", self)
        home_btn.move(30, 140)
        
        btn1_add.clicked.connect(self.buttonClicked)            
        btn1_sub.clicked.connect(self.buttonClicked)            
        free_btn.clicked.connect(self.buttonClicked) 
        close_btn.clicked.connect(self.close) 
        home_btn.clicked.connect(self.home) 

        # ラベル作成、初期の名前をUbuntuにする
        self.lbl = QLabel("Servo id", self)

        # QComboBoxオブジェクトの作成
        combo = QComboBox(self)
        # アイテムの名前設定
        for id in range(1,10):
            combo.addItem(str(id))

        result_btn =QPushButton("Result", self)

        combo.move(30, 20)
        self.lbl.move(30, 60)
        result_btn.move(30, 100)
        
        self.statusBar()

        # アイテムが選択されたらonActivated関数の呼び出し
        combo.activated[str].connect(self.onActivated)        
        result_btn.clicked.connect(self.result) 

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()


    def onActivated(self, text):
        self.id = int(text)
        # ラベルに選択されたアイテムの名前を設定
        self.lbl.setText(text)
        # ラベルの長さを調整
        self.lbl.adjustSize()  
        print (self.aaa.setMode(self.id,"POSITION"))

    def motor_move(self):
        if self.id == 2 :
            self.pos[3] = -self.pos[2]
            print (self.aaa.positionCmd(2, self.pos[2], 1))
            print (self.aaa.positionCmd(3, self.pos[3], 1))
        elif self.id == 3 :
            self.pos[2] = -self.pos[3]
            print (self.aaa.positionCmd(2, self.pos[2], 1))
            print (self.aaa.positionCmd(3, self.pos[3], 1))
        else:
            print (self.aaa.positionCmd(self.id, self.pos[self.id], 1))

    def close(self):
        print (self.aaa.setTrajectoryType(255,"EVEN"))
        print (self.aaa.setMode(255,"POSITION"))
        # self.pos = [0, 0, -14000, 14000, 8000, 9000, 0, 0, 0, 2000]
        self.pos =[0, 0, -14000, 14000, -28000, 7000, 0, 0, 0, 4000] 
        print(self.pos)
        
        for id in range(1,10):
            print (self.aaa.positionCmd(id, self.pos[id], 5))
    
    def home(self):
        print (self.aaa.setTrajectoryType(255,"EVEN"))
        print (self.aaa.setMode(255,"POSITION"))
        self.pos = [0, 0, 0, 0, 0, -9000, 0, 0, 0, 0]

        print(self.pos)
        
        for id in range(1,10):
            print (self.aaa.positionCmd(id, self.pos[id], 10))

    def buttonClicked(self):
        # ステータスバーへメッセージの表示
 
        sender = self.sender()

        if sender.text() == "+":
            self.pos[self.id] += 1000 
            if self.pos[self.id] >=32000:
                self.pos[self.id]=32000
            self.motor_move()

        elif sender.text() == "-":
            self.pos[self.id] -= 1000 
            if self.pos[self.id] <=-32000:
                self.pos[self.id]=-32000
            self.motor_move()

        if sender.text() == "FREE_MODE":
            print (self.aaa.setMode(self.id,"FREE"))

        else:
            pass
        self.statusBar().showMessage('id '+ str(self.id) + ' position is ' + str(self.pos[self.id]))

    def result(self):
        print(self.pos)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
