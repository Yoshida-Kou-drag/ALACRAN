import b3mCtrl
import time

aaa = b3mCtrl.B3mClass()
aaa.begin("COM3",1500000)

print(aaa.setMode(7,"FREE"))
time.sleep(0.01)

# print(aaa.setMode(7,"TORQUE"))
# time.sleep(0.01)

print(aaa.setMode(10,"FREE"))
time.sleep(0.01)

print(aaa.setMode(10,"TORQUE"))
time.sleep(0.01)

# hoge = aaa.setRam(7, 100, "DesiredTorque")
# time.sleep(0.01)
hoge = aaa.setRam(10, -100, "DesiredTorque")
time.sleep(0.01)

try :
    while True:
        torque = int(input("pls enter torque : "))

        if torque<20000 and torque>-20000:

            print("Torque is ",torque)
            # hoge = aaa.setRam(7, torque, "DesiredTorque")
            # time.sleep(0.01)
            hoge = aaa.setRam(10, torque, "DesiredTorque")
            time.sleep(0.01)
        else :
            print("ERROR : pls enter range -20000~20000")

except KeyboardInterrupt:
    print(aaa.setMode(255,"FREE"))
    time.sleep(0.01)