import b3mCtrl
import time


aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)

idx= [2]

for id in range(len(idx)):
    print(aaa.setMode(idx[id],"FREE"))
    time.sleep(0.01)
    
    print(aaa.setMode(idx[id],"SPEED"))
    time.sleep(0.01)
    
    hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
    time.sleep(0.01)

print("UP")
for id in range(len(idx)):
    hoge = aaa.setRam(idx[id], 10000, "DesiredVelosity")
    time.sleep(0.01)

time.sleep(3)

print("stop")
for id in range(len(idx)):
    hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
    time.sleep(0.01)

time.sleep(2)


print("down")
for id in range(len(idx)):
    hoge = aaa.setRam(idx[id], -10000, "DesiredVelosity")
    time.sleep(0.01)

time.sleep(3)

print("free")
for id in range(len(idx)):
    print(aaa.setMode(idx[id],"FREE"))
    time.sleep(0.01)