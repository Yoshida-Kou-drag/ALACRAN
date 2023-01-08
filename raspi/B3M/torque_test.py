import b3mCtrl
import time


aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)

idx= [4]

for id in range(len(idx)):

    #状態をFreeに
    print(aaa.setMode(idx[id],"FREE"))
    time.sleep(0.01)
    
    #制御モードをトルク制御に
    print(aaa.setMode(idx[id],"TORQUE"))
    time.sleep(0.01)

    
    hoge = aaa.getRam(idx[id], "GainPresetNo")
    time.sleep(0.01)
    print(hoge)
    #ゲイン設定
    hoge = aaa.setRam(idx[id], 2, "GainPresetNo")
    time.sleep(0.01)
    print(hoge)


while True:

    torque = int(input("pls ent trqv:"))
    
    for id in range(len(idx)):

        #目標トルクの指令
        hoge = aaa.setRam(idx[id], torque, "DesiredTorque")
        time.sleep(0.01)