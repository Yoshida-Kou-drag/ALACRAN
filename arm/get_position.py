#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time



if __name__ == '__main__':
    aaa = b3mCtrl.B3mClass()
    aaa.begin("/dev/ttyUSB0",1500000)
    
    # idx= [0]
    idx= [1,2,3,4,5,6,7,8,9]
    pos = [0]*10

    for id in idx:
        print("id = ",str(id))

        run =1
        while run: #原点の値を取得
            pos[id] = aaa.getRam(id,"CurrentPosition")

            if(pos[id][0] != False):
                print(pos[id][0])
                run=0
            if(pos[id][0] is not False):
                pass
    
    print("pos =",pos )