#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time


class B3m_init_error():
    def __init__(self):
        self.aaa = b3mCtrl.B3mClass()
        self.aaa.begin("/dev/ttyUSB0",1500000)

    def calibration (self,idx, pos):
        for id in idx:
            print("id = ",str(id))
            # input()
            run =1
            while run: #オフセットのリセット
                hoge = self.aaa.setRam(id, 0,"PositionCenterOffset")
                    
                if(hoge[0] != False):
                    print("hoge = ",hoge)
                    run=0
                if(hoge is not False):
                    #print(id)
                    pass
            run =1
            while run: #原点の値を取得
                hoge2 = self.aaa.getRam(id,"CurrentPosition")

                if(hoge2[0] != False):
                    if hoge2[0]>18000:
                        center=hoge2[0]-36000
                    elif hoge2[0]<-18000:
                        center=hoge2[0]+36000
                    else :
                        center=hoge2[0]
                    print("hoge2 = ",hoge2[0])
                    print("center = ",center)
                    run=0
                if(hoge2 is not False):
                    #print(id)
                    pass

            run=1
            while run: #取得した値をオフセット
                hoge = self.aaa.setRam(id, center,"PositionCenterOffset")
                    
                if(hoge[0] != False):
                    print("hoge = ",hoge)
                    run=0
                if(hoge is not False):
                    #print(id)
                    pass

            run=1
            while run: #確認
                hoge2 = self.aaa.getRam(id,"CurrentPosition")

                if(hoge2[0] != False):
                    print("CurrentPosition is ",hoge2[0])
                    run=0
                if(hoge2 is not False):
                    #print(id)
                    pass
                
        print("calib comp")

    def close(self):
        # self.pos = [0, 0, -14000, 14000, 8000, 9000, 0, 0, 0, 2000]
        self.pos =[0, 0, -1000, 1000, -28000, 7000, 0, 0, 0, 4000] 
        print(self.pos)
        
        for id in range(1,10):
            if id == 4:
                pass
            else :
                print (self.aaa.positionCmd(id, self.pos[id], 10))

    def pos_error_handler(self,id,calib_pos) :
        run =1
        while run: #原点の値を取得
            pos = self.aaa.getRam(id,"CurrentPosition")

            if(pos[0] != False):
                print(pos[0])
                run=0
            if(pos[0] is not False):
                pass
        
        self.calibration(id ,pos)
        print (self.aaa.setTrajectoryType(255,"EVEN"))
        print (self.aaa.setMode(255,"POSITION"))
        self.close()
        time.sleep(10)
        print (self.aaa.positionCmd(id,calib_pos, 10))
        time.sleep(10)

        print (self.aaa.setMode(255,"HOLD"))
        self.calibration(id ,pos)
        
        print (self.aaa.setTrajectoryType(255,"EVEN"))
        print (self.aaa.setMode(255,"POSITION"))
        print (self.aaa.positionCmd(id,-(calib_pos-2000), 10))
        time.sleep(10)

        # print (self.aaa.setMode(255,"FREE"))

if __name__ == '__main__':
    id = [4]
    check_motor = B3m_init_error()
    check_motor.pos_error_handler(id,30000)




    